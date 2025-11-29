from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.whatsapp_service import whatsapp_service

router = APIRouter()

class WhatsAppRequest(BaseModel):
    phone_number: str
    message: str
    media_url: Optional[str] = None

@router.post("/send")
async def send_whatsapp(request: WhatsAppRequest):
    """
    Send a WhatsApp message.
    """
    try:
        await whatsapp_service.send_assignment_result(
            phone_number=request.phone_number,
            message=request.message,
            media_url=request.media_url
        )
        return {"success": True, "message": "WhatsApp message sent successfully (placeholder)"}
    except NotImplementedError:
        return {
            "success": True, 
            "message": f"WhatsApp message simulated to {request.phone_number}",
            "data": {
                "message": request.message,
                "media_url": request.media_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
