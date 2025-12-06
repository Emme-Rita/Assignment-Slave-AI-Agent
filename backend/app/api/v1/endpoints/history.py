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
