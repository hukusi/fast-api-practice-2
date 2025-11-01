from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from models import Users

models.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]
        
router = APIRouter(
    prefix='/user',
    tags=['user']
)

# @router.get("/")
# def health_check():
#     return {'status': 'user'}


@router.get('/')
async def get_user(username, db: db_dependency):
    if username is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(Users).filter(Users.username == username).first()

