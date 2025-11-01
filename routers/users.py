from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from typing import Annotated, List
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from models import User as UserModel
from schemas import User as UserSchema, UserCreate

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

@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(
        name=user.name,
        age=user.age,
        gender=user.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user