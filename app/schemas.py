from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, Dict, Any

class EmotionInput(BaseModel):
    emotion: str
    timestamp: Optional[datetime] = None
    image_path: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[str] = None
    meta_info: Optional[Dict[str, Any]] = None

class EmotionOutput(BaseModel):
    id: int
    emotion: str
    timestamp: datetime
    image_path: Optional[str]
    source: Optional[str]
    confidence: Optional[str]
    meta_info: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True

class AggregationOutput(BaseModel):
    date: date
    emotion: str
    count: int

    class Config:
        orm_mode = True
