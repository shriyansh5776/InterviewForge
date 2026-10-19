from pydantic import BaseModel,EmailStr
from typing import Optional
class UserCreate(BaseModel):
    email : EmailStr
    password:str
    full_name : str
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name : Optional[str] = None
    
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str