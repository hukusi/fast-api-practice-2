from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Staff
from schemas import Staff
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import User as UserModel
from schemas import User as UserSchema, UserCreate
from typing import Annotated
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from starlette import status

SECRET_KEY ="5722b250fd0397914153b81a7d5a622a913e432dd447a68c658cff81e2956386"
ALGORITHM = 'HS256'

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

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

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not validateuser')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not validate user.')

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.email == email).first()
    if not staff or not pwd_context.verify(password, staff.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "staff_id": staff.id, "role": staff.role}

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(
        name=user.name,
        age=user.age,
        gender=user.gender,
        role=user.role,
        password=pwd_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not validate user.')
    token = create_access_token(user.name, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'toke_type': 'bearer'}





