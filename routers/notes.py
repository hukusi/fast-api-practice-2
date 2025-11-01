from fastapi import APIRouter
from database import SessionLocal

import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
router = APIRouter(
    prefix='/note',
    tags=['note']
)

@router.get("/")
def health_check():
    return {'status': 'note'}

