from sqlalchemy import Column, String, Text, DateTime, Boolean, Float
import uuid
from datetime import datetime
from app.db.session import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, default="New Conversation")
    prompt = Column(Text, nullable=True)
    file_name = Column(String, nullable=True)
    audio_file_path = Column(String, nullable=True)
    response_json = Column(Text, nullable=True) # Storing JSON as text
    school_name = Column(String, nullable=True)
    
    # Metadata fields
    student_level = Column(String, nullable=True)
    department = Column(String, nullable=True)
    submission_format = Column(String, nullable=True)
    
    # Agent Flags
    use_research = Column(Boolean, default=False)
    stealth_mode = Column(Boolean, default=False)
    style_mirrored = Column(Boolean, default=False)
    
    # Verification & Delivery
    trust_score = Column(Float, nullable=True)
    verification_json = Column(Text, nullable=True)
    research_context = Column(Text, nullable=True) # Storing raw research notes
    file_generated = Column(String, nullable=True)
    email_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
