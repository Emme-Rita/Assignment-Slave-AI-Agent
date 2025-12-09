import sys
import os
sys.path.append(os.getcwd())
from app.db.session import SessionLocal
from app.models.conversation import Conversation
from sqlalchemy import text

def check_count():
    db = SessionLocal()
    try:
        # Check raw count
        count = db.query(Conversation).count()
        print(f"DEBUG_DB_COUNT: {count}")
        
        # Check file path of DB
        db_path = os.path.abspath("app.db")
        print(f"DEBUG_DB_PATH: {db_path}")
        print(f"DEBUG_DB_EXISTS: {os.path.exists(db_path)}")
        
    except Exception as e:
        print(f"DEBUG_ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_count()
