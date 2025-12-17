import sqlite3
import os

def check_schema():
    db_path = "app.db"
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {tables}")
        
        if ('conversations',) in tables:
            cursor.execute("SELECT count(*) FROM conversations")
            count = cursor.fetchone()[0]
            print(f"Row count in conversations: {count}")
            
            # Check columns
            cursor.execute("PRAGMA table_info(conversations)")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(col)
        else:
            print("Table 'conversations' NOT found.")
            
        conn.close()
    except Exception as e:
        print(f"Error inspecting DB: {e}")

if __name__ == "__main__":
    check_schema()
