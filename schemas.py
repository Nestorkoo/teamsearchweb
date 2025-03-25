from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    name: str
    email: EmailStr
    skills: Optional[str] = None
    interests: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class UserCreate(UserBase):
    password: str  # Пароль тільки при створенні

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True