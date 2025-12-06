import sys
import os
sys.path.append(os.getcwd())

try:
    from app.services.search_service import search_service
    print("Search service imported successfully")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Other Error: {e}")
