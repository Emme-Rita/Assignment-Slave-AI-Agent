import asyncio
import sys
import os

# dynamic path append to find app module
sys.path.append(os.getcwd())

from app.services.history_service import history_service
from app.db.session import engine, Base

async def test_save():
    print("Testing History Save...")
    
    # 1. Ensure tables exist (just in case)
    Base.metadata.create_all(bind=engine)
    print("Tables ensured.")

    # 2. Dummy Data
    dummy_data = {
        "prompt": "Test Prompt",
        "student_level": "University",
        "department": "CS",
        "submission_format": "text",
        "use_research": False,
        "stealth_mode": False,
        "style_mirrored": False,
        "email_sent": False,
        "file_generated": None,
        "result": {
            "title": "Test Title",
            "answer": "Test Answer"
        }
    }

    # 3. Attempt Save
    try:
        record_id = await history_service.save_execution(dummy_data)
        if record_id:
            print(f"SUCCESS: Saved record {record_id}")
        else:
            print("FAILURE: save_execution returned None")
    except Exception as e:
        with open("debug_log.txt", "w") as f:
            f.write(f"CRITICAL FAILURE: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        print("Logged error to debug_log.txt")

    # 4. Verify Read
    try:
        records = await history_service.get_all_history(1)
        print(f"Found {len(records)} records.")
        if records:
            print(f"Latest: {records[0]}")
    except Exception as e:
         print(f"Read Failure: {e}")

if __name__ == "__main__":
    asyncio.run(test_save())
