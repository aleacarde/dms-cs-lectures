from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    legal_name: str
    preferred_name: Optional[str] = None

class UserCreate(UserBase):
    password: str  # Password is only required during creation

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
