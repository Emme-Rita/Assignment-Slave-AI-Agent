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
                import pygetwindow as gw
                import win32gui
                import win32con
                from urllib.parse import quote
                
                # 1. Copy file to clipboard using PowerShell 
                cmd = f'powershell -command "Set-Clipboard -Path \'{abs_path}\'"'
                subprocess.run(cmd, shell=True, check=True)
                logger.info("File copied to clipboard via PowerShell.")
                
                # 2. Open WhatsApp Chat directly
                url = f"https://web.whatsapp.com/send?phone={recipient_number}"
                webbrowser.open(url)
                
                # 3. Wait for load (Increased to 35s to be absolutely safe for slow loads)
                logger.info("Waiting 35 seconds for WhatsApp Web to fully load and resolve 'Starting chat'...")
                sleep(35)
                
                # 4. Attempt to focus the window using win32gui (more robust than pygetwindow)
                def window_enum_handler(hwnd, ctx):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if 'whatsapp' in title.lower():
                            ctx.append((hwnd, title))

                wa_windows = []
                win32gui.EnumWindows(window_enum_handler, wa_windows)
                
                if wa_windows:
                    hwnd, title = wa_windows[0]
                    logger.info(f"Found window: '{title}'. Bringing to foreground.")
                    try:
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                        win32gui.SetForegroundWindow(hwnd)
                        sleep(2)
                    except Exception as e:
                        logger.warning(f"SetForegroundWindow failed: {e}. Trying simple click.")
                
                # 5. Clear any blocking overlays or 'Starting chat' banner
                # Pressing Esc twice to be sure any modal or banner is cleared
                pyautogui.press('esc')
                sleep(1)
                pyautogui.press('esc')
                sleep(1)

                # 6. Force focus by clicking the input area
                # In WA Web, the input area is usually in the bottom 10% of the window
                try:
                    windows = [w for w in gw.getAllWindows() if 'WhatsApp' in w.title or 'WhatsApp' in w.title.lower()]
                    if windows:
                        w = windows[0]
                        # Click about 80 pixels above bottom center to hit the message box
                        focus_x = w.left + (w.width // 2)
                        focus_y = (w.top + w.height) - 80
                        logger.info(f"Clicking input area at ({focus_x}, {focus_y}) to ensure focus.")
                        pyautogui.click(focus_x, focus_y)
                        sleep(1)
                except:
                    pass

                # 7. Paste file
                logger.info("Pasting file (Ctrl+V)...")
                pyautogui.hotkey('ctrl', 'v')
                
                # 8. Wait for File Preview Modal to appear (it takes a second to process the file)
                sleep(8)
                
                # 9. Type Caption (if exists) 
                if caption:
                    logger.info(f"Typing caption: {caption}")
                    pyautogui.write(caption, interval=0.03)
                    sleep(2)
                
                # 10. Send
                logger.info("Pressing Enter to send...")
                pyautogui.press('enter')
                
                # Give it a moment to actually send
                sleep(5)
                return True
                
            except Exception as e:
                logger.error(f"File send error: {e}")
                import traceback
                logger.error(traceback.format_exc())
                return False

        return await asyncio.to_thread(_send_file_logic)

whatsapp_service = WhatsAppService()
