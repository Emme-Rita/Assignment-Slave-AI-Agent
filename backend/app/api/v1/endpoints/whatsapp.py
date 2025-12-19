from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.whatsapp_service import whatsapp_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class WhatsAppRequest(BaseModel):
    phone_number: str
    message: str
    media_url: Optional[str] = None

@router.post("/whatsapp", response_model=dict)
async def send_whatsapp(request: WhatsAppRequest):
    """
    Send a WhatsApp message using pywhatkit browser automation.
    """
    try:
        # If media_url is provided, treat it as a file path and send file
        if request.media_url:
            success = await whatsapp_service.send_file(
                recipient_number=request.phone_number,
                file_path=request.media_url,
                caption=request.message
            )
        else:
            # Send text message only
            success = await whatsapp_service.send_notification(
                recipient_number=request.phone_number,
                message=request.message
            )
        
        if success:
            return {"success": True, "message": "WhatsApp message sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
            
    except Exception as e:
        logger.error(f"WhatsApp endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
