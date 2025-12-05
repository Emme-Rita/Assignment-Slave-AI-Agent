from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.whatsapp_service import whatsapp_service

router = APIRouter()

class WhatsAppRequest(BaseModel):
    phone_number: str
    message: str
    media_url: Optional[str] = None

@router.post("/whatsapp", response_model=dict)
async def send_whatsapp(request: WhatsAppRequest):
    """
    Send a WhatsApp message using Meta Graph API.
    """
    try:
        response = await whatsapp_service.send_assignment_result(
            phone_number=request.phone_number,
            message=request.message,
            media_url=request.media_url
        )
        return {"success": True, "message": "WhatsApp message sent", "api_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
