import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        # We no longer strictly need these to be set for pywhatkit, 
        # but we might want to check if a phone number is valid in the request.
        self.enabled = True 
        try:
            import pywhatkit
            self.kit = pywhatkit
        except ImportError:
            logger.error("pywhatkit not installed. WhatsApp service disabled.")
            self.enabled = False

    async def send_notification(self, recipient_number: str, message: str):
        """
        Sends a text message using WhatsApp Web automation (pywhatkit).
        """
        if not self.enabled:
            logger.error("WhatsApp Service is disabled (pywhatkit missing).")
            return False

        if not recipient_number.startswith("+"):
            # Ensure number has international format (e.g., +1234567890)
            # This is a basic guess, user should provide full number.
            recipient_number = "+" + recipient_number

        logger.info(f"Attempting to send WhatsApp message to {recipient_number} via Browser...")
        
        # pywhatkit.sendwhatmsg_instantly is a blocking call that controls the mouse/keyboard.
        # We run it in a thread to avoid blocking the async event loop entirely,
        # though it will still seize control of the user's GUI session.
        import asyncio
        
        def _send():
            try:
                # wait_time=15 (seconds to load WA Web), tab_close=True, close_time=3
                self.kit.sendwhatmsg_instantly(recipient_number, message, 15, True, 3)
                return True
            except Exception as e:
                logger.error(f"pywhatkit error: {e}")
                return False

        try:
            # Run the blocking function in a separate thread
            return await asyncio.to_thread(_send)
        except Exception as e:
            logger.error(f"Failed to execute pywhatkit: {e}")
            return False

    async def send_file(self, recipient_number: str, file_path: str, caption: str = ""):
        """
        Sends a file using WhatsApp Web automation by copying it to clipboard and pasting.
        """
        if not self.enabled:
            return False

        if not recipient_number.startswith("+"):
            recipient_number = "+" + recipient_number

        import asyncio
        import subprocess
        import os
        from time import sleep

        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            logger.error(f"File not found: {abs_path}")
            return False
            
        logger.info(f"Sending file {abs_path} to {recipient_number}...")

        def _send_file_logic():
            try:
                import pyautogui
                import webbrowser
                from urllib.parse import quote
                
                # 1. Copy file to clipboard using PowerShell (LiteralPath handles spaces/chars better)
                # We use multiple formats to ensure compatibility
                cmd = f'powershell -command "Set-Clipboard -LiteralPath \'{abs_path}\'"'
                subprocess.run(cmd, shell=True, check=True)
                logger.info("File copied to clipboard.")
                
                # 2. Open WhatsApp Chat directly
                # bypassing pywhatkit.sendwhatmsg which types/sends text automatically
                url = f"https://web.whatsapp.com/send?phone={recipient_number}"
                webbrowser.open(url)
                
                # 3. Wait for load (User reported 5 mins, but that was likely failure to act, not load time)
                # We'll wait 20s for the page to render and the "Starting chat" overlay to clear
                sleep(20)
                
                # 4. Ensure focus (Clicking near the input bar area)
                # It's hard to guess coordinates, but usually the chat input is at the bottom.
                # Ctrl+F to focus search, then Tab? Or just Tab until focus?
                # Usually opening the link focuses the chat input automatically.
                # Let's try attempting Paste directly first.
                
                logger.info("Pasting file...")
                pyautogui.hotkey('ctrl', 'v')
                
                # 5. Wait for File Preview Modal
                # This is critical. If paste worked, a modal appears.
                sleep(5)
                
                # 6. Type Caption (if exists) 
                # When preview is open, focus is usually in the "Add a caption" box.
                if caption:
                    pyautogui.write(caption)
                    sleep(2)
                
                # 7. Send
                pyautogui.press('enter')
                return True
                
            except Exception as e:
                logger.error(f"File send error: {e}")
                return False

        return await asyncio.to_thread(_send_file_logic)

whatsapp_service = WhatsAppService()
