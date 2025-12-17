import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.api_token = settings.WHATSAPP_API_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        self.enabled = bool(self.api_token and self.phone_number_id)
        if not self.enabled:
             logger.warning("WhatsApp Service: Disabled (Missing Credentials). Messages will be mocked.")

    async def send_notification(self, recipient_number: str, message: str):
        """
        Sends a text message to the specified WhatsApp number.
        """
        if not self.enabled:
            print(f"[`MOCK WHATSAPP`] To: {recipient_number} | Message: {message}")
            return True

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "text",
            "text": {"body": message},
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, headers=self.headers, json=payload)
                response.raise_for_status()
                logger.info(f"WhatsApp message sent to {recipient_number}")
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to send WhatsApp message: {e.response.text}")
                return False
            except Exception as e:
                logger.error(f"WhatsApp service error: {str(e)}")
                return False

whatsapp_service = WhatsAppService()
