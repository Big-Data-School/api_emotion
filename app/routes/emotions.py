from typing import List
from datetime import datetime
from fastapi import APIRouter
from app.database import SessionLocal
from app.models import EmotionDB, AggregationDB
from app.schemas import EmotionInput, EmotionOutput, AggregationOutput

router = APIRouter()

@router.post("/detect", response_model=EmotionOutput)
def detect_emotion(data: EmotionInput):
    db = SessionLocal()
    record = EmotionDB(
        emotion=data.emotion,
        timestamp=data.timestamp or datetime.utcnow(),
        image_path=data.image_path,
        source=data.source,
        confidence=data.confidence,
        meta_info=data.meta_info,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return record

@router.get("/emotions", response_model=List[EmotionOutput])
def get_emotions():
    db = SessionLocal()
    results = db.query(EmotionDB).all()
    db.close()
    return results

@router.get("/aggregation", response_model=List[AggregationOutput])
def get_aggregation():
    db = SessionLocal()
    results = db.query(AggregationDB).all()
    db.close()
    return results
