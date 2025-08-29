# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    insight_type = Column(String, nullable=False)  # "ai" or "fallback"
    summary_text = Column(Text, nullable=True)
    top_words = Column(Text, nullable=True)  # JSON string of top words
