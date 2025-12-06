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
    
    async def send_assignment_result(
        self,
        recipient: str,
        subject: str,
        content: str,
        attachments: Optional[List[str]] = None
    ):
        """
        Send assignment result via email.
        
        Args:
            recipient: Email recipient
            subject: Email subject
            content: Email body content
            attachments: List of file paths to attach
        """
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
        await self.send_assignment_result(recipient, subject, content)

email_service = EmailService()
