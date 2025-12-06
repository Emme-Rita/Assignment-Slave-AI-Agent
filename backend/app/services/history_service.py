import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid

class HistoryService:
    def __init__(self):
        self.history_dir = os.path.join(os.getcwd(), "history")
        os.makedirs(self.history_dir, exist_ok=True)
    
    async def save_execution(self, execution_data: Dict) -> str:
        """
        Save an assignment execution to history.
        
        Args:
            execution_data: Dictionary containing execution details
            
        Returns:
            ID of the saved record
        """
        try:
            print(f"[HISTORY] Attempting to save execution...")
            print(f"[HISTORY] History directory: {self.history_dir}")
            
            record_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Create metadata record
            metadata = {
                "id": record_id,
                "timestamp": timestamp,
                "prompt": execution_data.get("prompt", ""),
                "student_level": execution_data.get("student_level", ""),
                "department": execution_data.get("department", ""),
                "submission_format": execution_data.get("submission_format", ""),
                "use_research": execution_data.get("use_research", False),
                "stealth_mode": execution_data.get("stealth_mode", False),
                "style_mirrored": execution_data.get("style_mirrored", False),
                "email_sent": execution_data.get("email_sent", False),
                "file_generated": execution_data.get("file_generated", None)
            }
            
            print(f"[HISTORY] Record ID: {record_id}")
            print(f"[HISTORY] Metadata: {metadata}")
            
            # Save metadata
            metadata_path = os.path.join(self.history_dir, f"{record_id}_metadata.json")
            print(f"[HISTORY] Saving metadata to: {metadata_path}")
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"[HISTORY] Metadata saved successfully")
            
            # Save full result if available
            if "result" in execution_data:
                result_path = os.path.join(self.history_dir, f"{record_id}_result.json")
                print(f"[HISTORY] Saving result to: {result_path}")
                with open(result_path, 'w', encoding='utf-8') as f:
                    json.dump(execution_data["result"], f, indent=2, ensure_ascii=False)
                print(f"[HISTORY] Result saved successfully")
            
            print(f"[HISTORY] Execution saved successfully with ID: {record_id}")
            return record_id
            
        except Exception as e:
            print(f"[HISTORY ERROR] Failed to save execution history: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_all_history(self, limit: int = 50) -> List[Dict]:
        """
        Retrieve all execution history records.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of history records sorted by timestamp (newest first)
        """
        try:
            records = []
            
            # Get all metadata files
            for filename in os.listdir(self.history_dir):
                if filename.endswith("_metadata.json"):
                    filepath = os.path.join(self.history_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        record = json.load(f)
                        records.append(record)
            
            # Sort by timestamp (newest first)
            records.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return records[:limit]
            
        except Exception as e:
            print(f"Failed to read history: {e}")
            return []
    
    async def get_execution_details(self, record_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific execution.
        
        Args:
            record_id: ID of the execution record
            
        Returns:
            Combined metadata and result data
        """
        try:
            metadata_path = os.path.join(self.history_dir, f"{record_id}_metadata.json")
            result_path = os.path.join(self.history_dir, f"{record_id}_result.json")
            
            if not os.path.exists(metadata_path):
                return None
            
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            result = None
            if os.path.exists(result_path):
                with open(result_path, 'r', encoding='utf-8') as f:
                    result = json.load(f)
            
            return {
                **metadata,
                "result": result
            }
            
        except Exception as e:
            print(f"Failed to read execution details: {e}")
            return None
    
    async def delete_execution(self, record_id: str) -> bool:
        """
        Delete an execution record from history.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            metadata_path = os.path.join(self.history_dir, f"{record_id}_metadata.json")
            result_path = os.path.join(self.history_dir, f"{record_id}_result.json")
            
            deleted = False
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
                deleted = True
            
            if os.path.exists(result_path):
                os.remove(result_path)
            
            return deleted
            
        except Exception as e:
            print(f"Failed to delete execution: {e}")
            return False

history_service = HistoryService()
