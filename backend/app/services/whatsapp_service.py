"""
WhatsApp Service - Future Implementation

This service will handle sending messages via WhatsApp.
"""

from typing import Optional

class WhatsAppService:
    """
    WhatsApp service for sending assignment results and notifications.
    
    Future implementation will include:
    - WhatsApp Business API integration
    - Message templates
    - Media message support
    - Status tracking
    """
    
    def __init__(self):
        # TODO: Initialize WhatsApp client (e.g., Twilio, WhatsApp Business API)
        pass
    
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
        # TODO: Implement WhatsApp sending logic
        raise NotImplementedError("WhatsApp service not yet implemented")
    
    async def send_notification(
        self,
        phone_number: str,
        message: str
    ):
        """
        Send a simple notification via WhatsApp.
        
        Args:
            phone_number: Recipient's phone number
            message: Notification message
        """
        # TODO: Implement notification logic
        raise NotImplementedError("WhatsApp service not yet implemented")

whatsapp_service = WhatsAppService()
