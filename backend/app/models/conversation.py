from sqlalchemy import Column, String, Text, DateTime
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
    created_at = Column(DateTime, default=datetime.utcnow)
