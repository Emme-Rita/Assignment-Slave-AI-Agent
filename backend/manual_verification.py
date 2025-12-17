import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.core.config import settings
from app.services.whatsapp_service import whatsapp_service
from app.services.email_service import email_service

async def verify():
    print("=== Configuration Verification ===")
    
    # 1. Check WhatsApp
    print(f"\n[WhatsApp] Enabled: {whatsapp_service.enabled}")
    if whatsapp_service.enabled:
        print("   ✅ pywhatkit is installed and ready.")
        print("   NOTE: Sending requires an active browser session with WhatsApp Web logged in.")
    else:
        print("   ❌ pywhatkit not found or disabled.")

    # 2. Check Email
    print(f"\n[Email] Enabled: {email_service.enabled}")
    if email_service.enabled:
        print(f"   ✅ Credentials found for: {settings.MAIL_USERNAME}")
        print(f"   Server: {settings.MAIL_SERVER}:{settings.MAIL_PORT}")
    else:
        print("   ❌ Email disabled. Missing MAIL_USERNAME/PASSWORD.")

    # 3. Test Action
    if whatsapp_service.enabled or email_service.enabled:
        choice = input("\nDo you want to attempt sending a test message? (y/n): ")
        if choice.lower() == 'y':
            target = input("Enter target (Phone for WA, Email for Mail): ")
            
            if "@" in target and email_service.enabled:
                print(f"Sending email to {target}...")
                try:
                    await email_service.send_notification(target, "Test Subject", "This is a test from Assignment Cheat.")
                    print("   ✅ Email Sent (Check inbox).")
                except Exception as e:
                    print(f"   ❌ Email Failed: {e}")
            
            elif whatsapp_service.enabled:
                print(f"Sending WhatsApp to {target}...")
                print("   ⚠️  Browser will open in 15 seconds. Do not touch mouse/keyboard.")
                try:
                    await whatsapp_service.send_notification(target, "This is a test message.")
                    print("   ✅ WhatsApp Command Executed.")
                except Exception as e:
                    print(f"   ❌ WhatsApp Failed: {e}")
            else:
                print("Target doesn't match available services.")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(verify())
    except KeyboardInterrupt:
        print("\nAborted.")
