import os
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv(dotenv_path=".env.local")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT")
DB_NAME     = os.getenv("DB_NAME")

# Construire l'URL de connexion PostgreSQL
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Configuration SQLAlchemy
engine       = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base         = declarative_base()

# --- Modèles de base de données ------------------------------------------------

class EmotionDB(Base):
    __tablename__ = "emotions"

    id         = Column(Integer, primary_key=True, index=True)
    emotion    = Column(String, nullable=False)
    timestamp  = Column(DateTime, default=datetime.utcnow)
    image_path = Column(String, nullable=True)
    source     = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    meta_info  = Column(JSONB, nullable=True)  # anciennement metadata

class AggregationDB(Base):
    __tablename__ = "aggregation"

    date    = Column(Date, primary_key=True)
    emotion = Column(String(20), primary_key=True)
    count   = Column(Integer, nullable=False)


# Création automatique des tables
Base.metadata.create_all(bind=engine)

# --- Initialisation de FastAPI ------------------------------------------------

app = FastAPI()


# --- Schémas Pydantic ---------------------------------------------------------

class EmotionInput(BaseModel):
    emotion: str
    timestamp: Optional[datetime] = None
    image_path: Optional[str]      = None
    source: Optional[str]          = None
    confidence: Optional[str]      = None
    meta_info: Optional[Dict[str, Any]] = None

class EmotionOutput(BaseModel):
    id: int
    emotion: str
    timestamp: datetime
    image_path: Optional[str]
    source: Optional[str]
    confidence: Optional[str]
    meta_info: Optional[Dict[str, Any]]

class AggregationOutput(BaseModel):
    date: date
    emotion: str
    count: int


# --- Endpoints ----------------------------------------------------------------

@app.post("/detect", response_model=EmotionOutput)
def detect_emotion(data: EmotionInput):
    db      = SessionLocal()
    record  = EmotionDB(
        emotion    = data.emotion,
        timestamp  = data.timestamp or datetime.utcnow(),
        image_path = data.image_path,
        source     = data.source,
        confidence = data.confidence,
        meta_info  = data.meta_info
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return record


@app.get("/emotions", response_model=List[EmotionOutput])
def get_emotions():
    db        = SessionLocal()
    results   = db.query(EmotionDB).all()
    db.close()
    return results


@app.get("/aggregation", response_model=List[AggregationOutput])
def get_aggregation():
    db      = SessionLocal()
    results = db.query(AggregationDB).all()
    db.close()
    return results
