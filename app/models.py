from app.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, DateTime, Date

class EmotionDB(Base):
    __tablename__ = "emotions"
    id         = Column(Integer, primary_key=True, index=True)
    emotion    = Column(String, nullable=False)
    timestamp  = Column(DateTime, default=datetime.utcnow)
    image_path = Column(String, nullable=True)
    source     = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    meta_info  = Column(JSONB, nullable=True)

class AggregationDB(Base):
    __tablename__ = "aggregation"
    date    = Column(Date, primary_key=True)
    emotion = Column(String(20), primary_key=True)
    count   = Column(Integer, nullable=False)
