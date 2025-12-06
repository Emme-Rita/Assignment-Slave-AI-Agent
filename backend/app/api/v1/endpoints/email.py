from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, List
from app.services.email_service import email_service
import shutil
import os
import uuid

router = APIRouter()

@router.post("/gmail", response_model=dict)
async def send_email(
    recipient: str = Form(...),
    subject: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None)
):
    """
    Send an email using the configured SMTP server.
    """
    try:
        attachments = []
        temp_file_path = None

        if file:
            # Create a temporary file to save the upload
            # We need to save it to disk because fastapi-mail expects a path
            temp_dir = "temp_uploads"
            os.makedirs(temp_dir, exist_ok=True)
            
            file_ext = os.path.splitext(file.filename)[1]
            temp_filename = f"{uuid.uuid4()}{file_ext}"
            temp_file_path = os.path.join(temp_dir, temp_filename)
            
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            attachments.append(temp_file_path)

        await email_service.send_assignment_result(
            recipient=recipient,
            subject=subject,
            content=content,
            attachments=attachments
        )
        
        # Cleanup temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass # Best effort cleanup
                
        return {"success": True, "message": f"Email sent to {recipient}"}
        return {"success": True, "message": f"Email sent to {request.recipient}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
