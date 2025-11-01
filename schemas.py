from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    age: int
    gender: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    notes: List[Note] = []
    created_at: datetime
    class Config:
        orm_mode = True


class StaffBase(BaseModel):
    email: str

class StaffCreate(StaffBase):
    password: str

class Staff(StaffBase):
    id: int
    role: str
    created_at: datetime
    class Config:
        orm_mode = True
