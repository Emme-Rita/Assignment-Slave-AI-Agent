from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, Union
from app.services.ai_service import ai_service
from app.services.file_service import file_service
from app.services.email_service import email_service
from app.services.humanizer_service import humanizer_service
from app.services.style_service import style_service
from app.services.history_service import history_service
from app.services.search_service import search_service
import base64
import json
import uuid
import os
import re

router = APIRouter()

@router.post("/analyze")
async def analyze_assignment(
    file: Optional[UploadFile] = File(None),
    prompt: Optional[str] = Form(None),
    use_research: bool = Form(True)
):
    """
    Analyze an assignment with AI assistance.
    
    Args:
        file: Assignment file (PDF, Word, or Image) - OPTIONAL
        prompt: User instructions (text or transcribed voice) - OPTIONAL
        use_research: Whether to perform web research before answering
    
    Returns:
        AI-generated response
    """
    try:
        # Validate that at least one input is provided
        if not file and not prompt:
            raise HTTPException(status_code=400, detail="Must provide either a file or a prompt")

        file_content = None
        
        # Process file if provided
        if file:
            # Validate file
            await file_service.validate_file(file)
            
            # Read file content
            file_bytes = await file.read()
            file_category = file_service.get_file_category(file.content_type)
            
            # Extract text from file if applicable
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
            # Local import to prevent NameError issues
            from app.services.search_service import search_service
            # Ensure query is not empty
            search_query = prompt if prompt and prompt.strip() else "Academic context for this assignment"
            research_results = await search_service.perform_research(search_query)
            context = research_results['summary']
        
        # Generate AI response
        response = await ai_service.generate_response(
            prompt=prompt,
            file_content=file_content,
            context=context
        )
        
        # Fact Check / Validation Guard
        verification_result = None
        if use_research:
             try:
                from app.services.fact_check_service import fact_check_service
                # Verify the raw response text
                verification_result = await fact_check_service.verify_content(response)
             except Exception as e:
                print(f"Fact check validation failed: {e}")

        # Save to history
        try:
            # Robust JSON extraction
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            response_json = json.loads(cleaned_response)
        except json.JSONDecodeError:
            try:
                # Try to find JSON object with regex
                match = re.search(r'\{.*\}', response, re.DOTALL)
                if match:
                    response_json = json.loads(match.group())
                else:
                    raise Exception("No JSON found")
            except:
                # Fallback structure
                response_json = {
                    "answer": response,
                    "title": "Analysis Result",
                    "question": prompt or "Assignment Analysis",
                    "summary": "See answer",
                    "note": "Could not parse structured response"
                }
            
        # Merge verification data
        if verification_result:
            response_json["verification"] = verification_result
        
        await history_service.save_execution({
            "prompt": prompt,
            "student_level": "University",
            "department": "General",
            "submission_format": "text",
            "use_research": use_research,
            "stealth_mode": False,
            "style_mirrored": False,
            "email_sent": False,
            "file_generated": None,
            "research_context": context,
            "result": response_json
        })
        
        return {
            "success": True,
            "response": response,
            "file_processed": file.filename if file else None,
            "research_used": use_research,
            "verification": verification_result
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit")
async def submit_assignment(
    image: Union[UploadFile, str, None] = File(None),
    voice: Union[UploadFile, str, None] = File(None),
    file: Union[UploadFile, str, None] = File(None), # Keep for backward compatibility or if they send 'file' instead of 'image'
    prompt: Optional[str] = Form(None) # Optional text prompt
):
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
                file_content = f"[Image file: {assignment_file.filename}]" 
                # NOTE: For true multimodal image analysis with Gemini, we should pass the image bytes.

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
        except json.JSONDecodeError:
            try:
                 # Try to find JSON object with regex
                match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
                if match:
                    response_data = json.loads(match.group())
                else:
                    raise Exception("No JSON found")
            except:
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
            
        # Ensure ID is present
        if "id" not in response_data or not response_data["id"]:
            response_data["id"] = str(uuid.uuid4())
            
        # Save to history
        await history_service.save_execution({
            "prompt": final_prompt,
            "student_level": "University", # Default
            "department": "General", # Default
            "submission_format": "text",
            "use_research": True, # Implied from logic
            "stealth_mode": False,
            "style_mirrored": False,
            "email_sent": False,
            "file_generated": None,
            "research_context": context,
            "result": response_data
        })
            
        return response_data

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute")
async def execute_assignment(
    file: Union[UploadFile, str, None] = File(None),
    image: Union[UploadFile, str, None] = File(None),
    voice: Union[UploadFile, str, None] = File(None),
    style_sample: Union[UploadFile, str, None] = File(None),
    prompt: str = Form(...),
    student_level: str = Form("University"),
    department: str = Form("General"),
    submission_format: str = Form("docx"),
    email: Optional[str] = Form(None),
    whatsapp: Optional[str] = Form(None),
    use_research: bool = Form(True),
    stealth_mode: bool = Form(False)
):
    """
    Full Agentic Execution Flow:
    1. Input Analysis (Assignment & Style Sample)
    2. Research
    3. Generation (with Student Profile & Style Mirroring)
    4. Stealth Mode (Humanization) [Optional]
    5. Formatting (PDF/Docx)
    6. Submission (Email & WhatsApp)
    """
    try:
        # 1. Input Processing
        if isinstance(image, str): image = None
        if isinstance(voice, str): voice = None
        if isinstance(file, str): file = None
        if isinstance(style_sample, str): style_sample = None
        
        assignment_file = image if image else file
        
        file_content = None
        audio_data = None
        style_instruction = None
        
        if assignment_file:
            await file_service.validate_file(assignment_file)
            file_bytes = await assignment_file.read()
            file_category = file_service.get_file_category(assignment_file.content_type)
            if file_category == 'pdf':
                file_content = ai_service.extract_text_from_pdf(file_bytes)
            elif file_category == 'word':
                file_content = ai_service.extract_text_from_docx(file_bytes)
            elif file_category == 'image':
                file_content = f"[Image file: {assignment_file.filename}]"

        # Process Style Sample (Doppelgänger)
        if style_sample:
            try:
                style_bytes = await style_sample.read()
                style_category = file_service.get_file_category(style_sample.content_type)
                style_text = ""
                if style_category == 'pdf':
                    style_text = ai_service.extract_text_from_pdf(style_bytes)
                elif style_category == 'word':
                    style_text = ai_service.extract_text_from_docx(style_bytes)
                else: 
                     # Attempt to read as text if unknown but likely text
                     try:
                        style_text = style_bytes.decode('utf-8')
                     except:
                        pass
                
                if style_text:
                    style_instruction = await style_service.analyze_style(style_text)
            except Exception as e:
                print(f"Style processing failed: {e}")

        if voice:
            voice_bytes = await voice.read()
            audio_data = {"data": voice_bytes, "mime_type": voice.content_type or "audio/mp3"}

        final_prompt = prompt if prompt else "Please solve this assignment."
        if voice: final_prompt += " (audio included)"
        
        # 2. Research Phase
        context = None
        research_summary = ""
        if use_research:
            try:
                # Local import for safety
                from app.services.search_service import search_service
                # Use a specific query derived from prompt or just the prompt
                research_results = await search_service.perform_research(final_prompt[:200])
                context = research_results.get('summary', '')
                research_summary = context
            except Exception as e:
                # Continue without research if it fails
                pass 

        # 3. Execution Phase (Generation)
        ai_response_text = await ai_service.generate_response(
            prompt=final_prompt,
            file_content=file_content,
            context=context,
            audio_data=audio_data,
            student_level=student_level,
            department=department,
            style_instruction=style_instruction
        )

        # Parse AI Response
        # Parse AI Response
        try:
            cleaned_response = ai_response_text.replace("```json", "").replace("```", "").strip()
            response_json = json.loads(cleaned_response)
        except json.JSONDecodeError:
            try:
                match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
                if match:
                    response_json = json.loads(match.group())
                else:
                    raise Exception("No JSON found")
            except:
                response_json = {"answer": ai_response_text}

        # Extract fields for processing
        answer_text = response_json.get("answer", ai_response_text)
        title = response_json.get("title", "Assignment Submission")
        question = response_json.get("question", "")
        summary = response_json.get("summary", "")

        # 4. Stealth Mode (Humanization)
        if stealth_mode:
            try:
                humanized_text = await humanizer_service.humanize_text(answer_text, student_level)
                # Update the answer text and the JSON response object
                answer_text = humanized_text
                response_json["answer"] = humanized_text
                # Add a metadata tag so frontend knows it was humanized
                response_json["humanized"] = True
            except Exception as e:
                print(f"Stealth mode failed: {e}")

        # 5. Formatting Phase
        generated_file_path = None
        filename = f"{uuid.uuid4()}.{submission_format}"
        
        try:
            # Construct Formatted Document Content
            document_content = f"Title: {title}\n"
            if question:
                document_content += f"\nQuestion / Topic:\n{question}\n"
            
            document_content += f"\n{'-'*20}\n"
            document_content += f"\nAnswer:\n\n{answer_text}\n"
            
            if summary:
                document_content += f"\n{'-'*20}\nSummary:\n{summary}\n"

            if submission_format.lower() == 'pdf':
                generated_file_path = file_service.generate_pdf(document_content, filename)
            else:
                generated_file_path = file_service.generate_docx(document_content, filename)
        except Exception as e:
            # File generation failed
            pass

        # 6. Submission Phase (Email & WhatsApp)
        email_sent = False
        whatsapp_sent = False
        
        if email and generated_file_path:
            try:
                await email_service.send_assignment_result(
                    recipient=email,
                    subject=f"Assignment Completed: {title}",
                    content=f"Your assignment '{title}' has been completed by Assignment Slave.\n\nLevel: {student_level}\nDepartment: {department}\nStealth Mode: {'Enabled' if stealth_mode else 'Disabled'}\nStyle Mirroring: {'Active' if style_instruction else 'Standard'}",
                    attachments=[generated_file_path]
                )
                email_sent = True
            except Exception as e:
                pass

        if whatsapp:
            try:
                from app.services.whatsapp_service import whatsapp_service
                msg = f"Assignment Slave: Your task '{title}' is complete!\nResult has been generated ({submission_format}).\nConfidence: High."
                if email_sent:
                    msg += f"\nFull document sent to {email}."
                
                await whatsapp_service.send_notification(whatsapp, msg)
                whatsapp_sent = True
            except Exception as e:
                print(f"WhatsApp error: {e}")

        # Save to history
        await history_service.save_execution({
            "prompt": prompt,
            "student_level": student_level,
            "department": department,
            "submission_format": submission_format,
            "use_research": use_research,
            "stealth_mode": stealth_mode,
            "style_mirrored": bool(style_instruction),
            "email_sent": email_sent,
            "file_generated": generated_file_path,
            "research_context": research_summary,
            "result": response_json
        })

        return {
            "success": True,
            "data": response_json,
            "research_context": research_summary,
            "file_generated": generated_file_path,
            "email_sent": email_sent,
            "whatsapp_sent": whatsapp_sent,
            "stealth_mode": stealth_mode,
            "style_mirrored": bool(style_instruction)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
