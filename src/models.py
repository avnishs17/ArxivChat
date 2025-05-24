"""
Simple data models for ArxivChat
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Paper(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    published: str
    pdf_url: str
    categories: List[str]

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None
