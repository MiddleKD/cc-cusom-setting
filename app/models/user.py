from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True

User = UserInDB

class MessageRequest(BaseModel):
    message: Optional[str] = "Hello World!"

class MessageResponse(BaseModel):
    message: str
    timestamp: datetime
    author: Optional[str] = None
    organization: Optional[str] = None