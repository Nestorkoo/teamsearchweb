from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    name: str
    email: EmailStr
    skills: Optional[str] = None
    interests: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    age: int = Field(..., ge=16, le=100, description="Age must be between 0 and 100")
    gender: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True