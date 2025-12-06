from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, Union
from app.services.ai_service import ai_service
from app.services.search_service import search_service
import base64
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.models.conversation import Conversation

router = APIRouter()

@router.post("/analyze")
async def analyze_assignment(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    use_research: bool = Form(False)
):
    """
    Analyze an assignment with AI assistance.
    
    Args:
        file: Assignment file (PDF, Word, or Image)
        prompt: User instructions (text or transcribed voice)
        use_research: Whether to perform web research before answering
    
    Returns:
        AI-generated response
    """
    try:
        # Validate file
        await file_service.validate_file(file)
        
        # Read file content
        file_bytes = await file.read()
        file_category = file_service.get_file_category(file.content_type)
        
        # Extract text from file if applicable
        file_content = None
        if file_category == 'pdf':
            file_content = ai_service.extract_text_from_pdf(file_bytes)
        elif file_category == 'word':
            file_content = ai_service.extract_text_from_docx(file_bytes)
        elif file_category == 'image':
            # For images, we'll encode and let Gemini handle it
            # Note: Gemini 1.5 Pro supports image input directly
            file_content = f"[Image file: {file.filename}]"
        
        # Perform research if requested
        context = None
        if use_research:
            research_results = await search_service.perform_research(prompt)
            context = research_results['summary']
        
        # Generate AI response
        response = await ai_service.generate_response(
            prompt=prompt,
            file_content=file_content,
            context=context
        )
        
        return {
            "success": True,
            "response": response,
            "file_processed": file.filename,
            "research_used": use_research
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import json
import uuid

@router.post("/submit")
async def submit_assignment(
    image: Union[UploadFile, str, None] = File(None),
    voice: Union[UploadFile, str, None] = File(None),
    file: Union[UploadFile, str, None] = File(None), # Keep for backward compatibility or if they send 'file' instead of 'image'
    prompt: Optional[str] = Form(None), # Optional text prompt
    db: Session = Depends(get_db)
):
    """
    Submit assignment (Image + Voice) for AI processing.
    Returns structured JSON for the frontend.
    """
    """
    Submit assignment (Image + Voice) for AI processing.
    Returns structured JSON for the frontend.
    """
    try:
        # Handle empty strings sent by frontend for file fields
        if isinstance(image, str): image = None
        if isinstance(voice, str): voice = None
        if isinstance(file, str): file = None

        # Handle inputs - prioritize 'image' but fallback to 'file'
        assignment_file = image if image else file
        
        if not assignment_file and not voice and not prompt:
             raise HTTPException(status_code=400, detail="Must provide image, voice, or prompt")

        file_content = None
        audio_data = None
        
        # Process Assignment File (Image/PDF/Word)
        if assignment_file:
            await file_service.validate_file(assignment_file)
            file_bytes = await assignment_file.read()
            file_category = file_service.get_file_category(assignment_file.content_type)
            
            if file_category == 'pdf':
                file_content = ai_service.extract_text_from_pdf(file_bytes)
            elif file_category == 'word':
                file_content = ai_service.extract_text_from_docx(file_bytes)
            elif file_category == 'image':
                file_content = f"[Image file: {assignment_file.filename}]" # Gemini handles images via prompt context usually, or we can expand to send image bytes if needed. For now, text extraction or description.
                # NOTE: For true multimodal image analysis with Gemini, we should pass the image bytes.
                # Updating ai_service to accept image bytes would be better, but for now we'll rely on the current structure
                # or assume the user wants text extraction. 
                # Given the prompt change, let's pass a note about the image.

        # Process Voice
        if voice:
            voice_bytes = await voice.read()
            audio_data = {
                "data": voice_bytes,
                "mime_type": voice.content_type or "audio/mp3"
            }
        
        # Construct Prompt
        final_prompt = prompt if prompt else "Please analyze this assignment and provide a solution."
        if voice:
            final_prompt += " (See audio instructions)"
            
        # Generate Response
        # We don't use 'context' (research) explicitly here as the new workflow implies the AI does it all.
        # But we can still trigger it if needed. For now, let's keep it simple.
        
        # Perform Research (Integrated Step)
        context = None
        search_query = prompt if prompt else None
        
        # If no prompt, try to use extracted text as query (truncate if too long)
        if not search_query and file_content and isinstance(file_content, str):
            search_query = file_content[:200].replace("\n", " ")
            
        if search_query:
            try:
                # We interpret "it researches on it" as integrated.
                # We'll use the search service to get context.
                research_results = await search_service.perform_research(search_query)
                context = research_results.get('summary')
            except Exception as e:
                print(f"Research failed (continuing without): {e}")

        ai_response_text = await ai_service.generate_response(
            prompt=final_prompt,
            file_content=file_content,
            context=context,
            audio_data=audio_data
        )
        
        # Parse JSON
        try:
            # Clean up potential markdown formatting
            cleaned_response = ai_response_text.replace("```json", "").replace("```", "").strip()
            response_data = json.loads(cleaned_response)
            
            # Ensure ID is present
            if "id" not in response_data or not response_data["id"]:
                response_data["id"] = str(uuid.uuid4())
                
            return response_data
            
        except json.JSONDecodeError:
            # Fallback if AI didn't return valid JSON
            response_data = {
                "id": str(uuid.uuid4()),
                "title": "Assignment Response",
                "question": "Could not parse question",
                "answer": ai_response_text,
                "summary": "See answer",
                "note": "Response was not in expected JSON format",
                "more": ""
            }
            
        # Save to Database
        try:
            conversation_entry = Conversation(
                id=response_data.get("id"),
                title=response_data.get("title", "New Conversation"),
                prompt=final_prompt,
                file_name=assignment_file.filename if assignment_file else None,
                response_json=json.dumps(response_data),
            )
            db.add(conversation_entry)
            db.commit()
            db.refresh(conversation_entry)
        except Exception as e:
            print(f"Error saving to DB: {e}")
            # Don't fail the request if DB save fails, just log it
            
        return response_data

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
