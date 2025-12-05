import requests
from app.core.config import settings
from typing import Optional

class WhatsAppService:
    """
    WhatsApp service for sending assignment results and notifications.
    Uses Meta Graph API (WhatsApp Business API).
    """
    
    def __init__(self):
        self.api_token = settings.WHATSAPP_API_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def send_assignment_result(
        self,
        phone_number: str,
        message: str,
        media_url: Optional[str] = None
    ):
        """
        Send assignment result via WhatsApp.
        
        Args:
            phone_number: Recipient's phone number (with country code)
            message: Message content
            media_url: Optional media attachment URL
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }
        
        if media_url:
            # If media is present, switch type to document or image
            # For simplicity, assuming document (PDF) for assignments
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "document",
                "document": {
                    "link": media_url,
                    "caption": message
                }
            }
            
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"WhatsApp API Error: {e}")
            if hasattr(e, 'response') and e.response:
                 print(f"Response: {e.response.text}")
            raise Exception(f"Failed to send WhatsApp message: {str(e)}")
    
    async def send_notification(
        self,
        phone_number: str,
        message: str
    ):
        """
        Send a simple notification via WhatsApp.
        """
        return await self.send_assignment_result(phone_number, message)

whatsapp_service = WhatsAppService()
