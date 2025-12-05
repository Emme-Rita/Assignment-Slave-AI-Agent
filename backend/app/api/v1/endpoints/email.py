from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.email_service import email_service

router = APIRouter()

class EmailRequest(BaseModel):
    recipient: str
    subject: str
    content: str
    attachments: Optional[List[str]] = None

@router.post("/gmail", response_model=dict)
async def send_email(request: EmailRequest):
    """
    Send an email using the configured SMTP server.
    """
    try:
        # In a real implementation, we would handle file attachments properly
        # For now, we just pass the list of filenames if they are paths
        await email_service.send_assignment_result(
            recipient=request.recipient,
            subject=request.subject,
            content=request.content,
            attachments=request.attachments
        )
        return {"success": True, "message": f"Email sent to {request.recipient}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
