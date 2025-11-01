from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Staff
from schemas import Staff
from passlib.context import CryptContext
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.email == email).first()
    if not staff or not pwd_context.verify(password, staff.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "staff_id": staff.id, "role": staff.role}