from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Staff
from schemas import Staff
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from models import User as UserModel
from typing import Annotated



router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(UserModel).filter(UserModel.name == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.email == email).first()
    if not staff or not pwd_context.verify(password, staff.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "staff_id": staff.id, "role": staff.role}


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Could not validate user.'
    return 'access_token'





