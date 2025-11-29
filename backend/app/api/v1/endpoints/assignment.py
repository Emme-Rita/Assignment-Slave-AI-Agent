from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.ai_service import ai_service
from app.services.file_service import file_service
from app.services.search_service import search_service
import base64

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


@router.post("/analyze-with-voice")
async def analyze_with_voice(
    file: UploadFile = File(...),
    voice_file: UploadFile = File(...),
    use_research: bool = Form(False)
):
    """
    Analyze an assignment with voice instructions.
    
    Args:
        file: Assignment file (PDF, Word, or Image)
        voice_file: Voice note (audio file)
        use_research: Whether to perform web research before answering
    
    Returns:
        AI-generated response
    """
    try:
        # Validate assignment file
        await file_service.validate_file(file)
        
        # Read files
        file_bytes = await file.read()
        voice_bytes = await voice_file.read()
        
        file_category = file_service.get_file_category(file.content_type)
        
        # Extract text from assignment file
        file_content = None
        if file_category == 'pdf':
            file_content = ai_service.extract_text_from_pdf(file_bytes)
        elif file_category == 'word':
            file_content = ai_service.extract_text_from_docx(file_bytes)
        elif file_category == 'image':
            file_content = f"[Image file: {file.filename}]"
        
        # Prepare audio data
        audio_data = {
            "data": voice_bytes,
            "mime_type": voice_file.content_type or "audio/mp3"
        }
        
        prompt = "Please listen to the voice instructions and help with the assignment."
        
        # Perform research if requested
        context = None
        if use_research:
            # For research, we need a text query. Since we don't have transcription yet,
            # we'll use a generic query or rely on the file content if possible.
            # Ideally, we'd transcribe first, then research.
            # For now, we'll skip specific research based on voice, or use a generic one.
            research_results = await search_service.perform_research(
                "General assignment help" 
            )
            context = research_results['summary']
        
        # Generate AI response with audio
        response = await ai_service.generate_response(
            prompt=prompt,
            file_content=file_content,
            context=context,
            audio_data=audio_data
        )
        
        return {
            "success": True,
            "response": response,
            "file_processed": file.filename,
            "voice_processed": voice_file.filename,
            "research_used": use_research
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
