"""
Email Service - Future Implementation

This service will handle sending emails with assignment results.
"""

from typing import Optional, List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """
    Email service for sending assignment results and notifications.
    Uses fastapi-mail for SMTP integration.
    """
    
    
    def __init__(self):
        self.enabled = bool(settings.MAIL_USERNAME and settings.MAIL_SERVER)
        if self.enabled:
            self.conf = ConnectionConfig(
                MAIL_USERNAME=settings.MAIL_USERNAME,
                MAIL_PASSWORD=settings.MAIL_PASSWORD,
                MAIL_FROM=settings.MAIL_FROM,
                MAIL_PORT=settings.MAIL_PORT,
                MAIL_SERVER=settings.MAIL_SERVER,
                MAIL_STARTTLS=True,
                MAIL_SSL_TLS=False,
                USE_CREDENTIALS=True,
                VALIDATE_CERTS=True
            )
            self.fastmail = FastMail(self.conf)
        else:
            print("Email Service: Disabled. Please set MAIL_USERNAME and MAIL_PASSWORD in .env for Gmail.")
    
    async def send_assignment_result(
        self,
        recipient: str,
        subject: str,
        content: str,
        attachments: Optional[List[str]] = None
    ):
        """
        Send assignment result via email.
        """
        if not self.enabled:
            print(f"[`MOCK EMAIL`] To: {recipient} | Subject: {subject} | Attachments: {attachments}")
            return

        try:
            message = MessageSchema(
                subject=subject,
                recipients=[recipient],
                body=content,
                subtype=MessageType.html,
                attachments=attachments
            )
            
            await self.fastmail.send_message(message)
            logger.info(f"Email sent successfully to {recipient}")
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {str(e)}")
            # For now, we raise it so the endpoint returns 500, or we could return False
            raise e
    
    async def send_notification(
        self,
        recipient: str,
        subject: str,
        content: str
    ):
        """
        Send a simple notification via email.
        """
        if not self.enabled:
            print(f"[`MOCK EMAIL`] To: {recipient} | Subject: {subject}")
            return

        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=content,
            subtype=MessageType.html
        )
        
        await self.fastmail.send_message(message)

email_service = EmailService()
