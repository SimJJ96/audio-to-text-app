from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Transcription(Base):
    __tablename__ = "transcriptions"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True, index=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.now)
