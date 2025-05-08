from fastapi import FastAPI
from app.routes import emotions
from app.database import Base, engine

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclure les routes
app.include_router(emotions.router)