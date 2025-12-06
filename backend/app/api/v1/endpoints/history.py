<<<<<<< HEAD
from fastapi import APIRouter, HTTPException
from app.services.history_service import history_service

router = APIRouter()

@router.get("/history")
async def get_history(limit: int = 50):
    """
    Get all assignment execution history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of history records
    """
    try:
        records = await history_service.get_all_history(limit=limit)
        return {
            "success": True,
            "data": records,
            "count": len(records)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{record_id}")
async def get_history_details(record_id: str):
    """
    Get detailed information about a specific execution.
    
    Args:
        record_id: ID of the execution record
        
    Returns:
        Detailed execution data
    """
    try:
        details = await history_service.get_execution_details(record_id)
        if not details:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {
            "success": True,
            "data": details
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{record_id}")
async def delete_history_record(record_id: str):
    """
    Delete an execution record from history.
    
    Args:
        record_id: ID of the record to delete
        
    Returns:
        Success status
    """
    try:
        deleted = await history_service.delete_execution(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {
            "success": True,
            "message": "Record deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.conversation import Conversation
import json

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all conversations (history).
    """
    conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).offset(skip).limit(limit).all()
    
    results = []
    for conv in conversations:
        results.append({
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "prompt": conv.prompt[:50] + "..." if conv.prompt and len(conv.prompt) > 50 else conv.prompt
        })
    return results

@router.get("/{conversation_id}", response_model=dict)
def read_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific conversation by ID.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Parse the stored JSON
    try:
        response_data = json.loads(conversation.response_json) if conversation.response_json else {}
    except:
        response_data = {"raw_content": conversation.response_json}
        
    return {
        "id": conversation.id,
        "title": conversation.title,
        "prompt": conversation.prompt,
        "file_name": conversation.file_name,
        "created_at": conversation.created_at,
        "response": response_data
    }
>>>>>>> da790a06c72ce82f237ad49c9726ece5c80e44dd
