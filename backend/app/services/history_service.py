from app.db.session import SessionLocal
from app.models.conversation import Conversation
from typing import List, Dict, Optional
import json
import uuid
from datetime import datetime

class HistoryService:
    def __init__(self):
        pass
    
    async def save_execution(self, execution_data: Dict) -> str:
        """
        Save an assignment execution to SQLite database.
        """
        db = SessionLocal()
        try:
            record_id = str(uuid.uuid4())
            
            # Prepare result JSON
            result_json = json.dumps(execution_data.get("result", {}))
            
            # Prepare verification JSON if present in result
            verification = execution_data.get("result", {}).get("verification", None)
            verification_json = json.dumps(verification) if verification else None
            
            trust_score = None
            if verification and isinstance(verification, dict):
                 trust_score = verification.get("trust_score")

            conversation = Conversation(
                id=record_id,
                title=execution_data.get("result", {}).get("title", "New Assignment"),
                prompt=execution_data.get("prompt", ""),
                
                # Metadata
                student_level=execution_data.get("student_level"),
                department=execution_data.get("department"),
                submission_format=execution_data.get("submission_format"),
                
                # Flags
                use_research=execution_data.get("use_research", False),
                stealth_mode=execution_data.get("stealth_mode", False),
                style_mirrored=execution_data.get("style_mirrored", False),
                
                # Delivery
                email_sent=execution_data.get("email_sent", False),
                file_generated=execution_data.get("file_generated"),
                
                # School
                school_name=execution_data.get("school_name"),
                
                # Verification
                trust_score=trust_score,
                verification_json=verification_json,
                research_context=execution_data.get("research_context"),
                
                # Payload
                response_json=result_json
            )
            
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            return conversation.id
            
        except Exception as e:
            print(f"[HISTORY ERROR] Failed to save execution to DB: {e}")
            db.rollback()
            return None
        finally:
            db.close()
    
    async def get_all_history(self, limit: int = 50) -> List[Dict]:
        """
        Retrieve all execution history records from DB.
        """
        db = SessionLocal()
        try:
            conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).limit(limit).all()
            
            records = []
            for conv in conversations:
                # Basic mapping for list view
                records.append({
                    "id": conv.id,
                    "timestamp": conv.created_at.isoformat(),
                    "title": conv.title,
                    "prompt": conv.prompt,
                    "student_level": conv.student_level,
                    "department": conv.department,
                    "submission_format": conv.submission_format,
                    "use_research": conv.use_research,
                    "stealth_mode": conv.stealth_mode,
                    "style_mirrored": conv.style_mirrored,
                    "email_sent": conv.email_sent,
                    "trust_score": conv.trust_score,
                    "school_name": conv.school_name
                })
            return records
            
        except Exception as e:
            print(f"Failed to read history from DB: {e}")
            return []
        finally:
            db.close()
    
    async def get_execution_details(self, record_id: str) -> Optional[Dict]:
        """
        Retrieve detailed record from DB.
        """
        db = SessionLocal()
        try:
            conv = db.query(Conversation).filter(Conversation.id == record_id).first()
            if not conv:
                return None
                
            # Reconstruct the full object structure expected by frontend
            result_data = json.loads(conv.response_json) if conv.response_json else {}
            
            # Inject stored verification data back into result if missing
            if conv.verification_json and "verification" not in result_data:
                try:
                    result_data["verification"] = json.loads(conv.verification_json)
                except: pass

            return {
                "id": conv.id,
                "timestamp": conv.created_at.isoformat(),
                "prompt": conv.prompt,
                "student_level": conv.student_level,
                "department": conv.department,
                "submission_format": conv.submission_format,
                "use_research": conv.use_research,
                "stealth_mode": conv.stealth_mode,
                "style_mirrored": conv.style_mirrored,
                "email_sent": conv.email_sent,
                "file_generated": conv.file_generated,
                "school_name": conv.school_name,
                "result": result_data
            }
            
        except Exception as e:
            print(f"Failed to read execution details from DB: {e}")
            return None
        finally:
            db.close()
    
    async def delete_execution(self, record_id: str) -> bool:
        """
        Delete a record from DB.
        """
        db = SessionLocal()
        try:
            conv = db.query(Conversation).filter(Conversation.id == record_id).first()
            if conv:
                db.delete(conv)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Failed to delete execution: {e}")
            db.rollback()
            return False
        finally:
            db.close()

history_service = HistoryService()
