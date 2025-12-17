import sqlite3
import os

def migrate_db():
    db_path = "app.db"
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(conversations)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'research_context' not in column_names:
            print("Adding missing column 'research_context'...")
            cursor.execute("ALTER TABLE conversations ADD COLUMN research_context TEXT DEFAULT NULL")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column 'research_context' already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Error migrating DB: {e}")

if __name__ == "__main__":
    migrate_db()
