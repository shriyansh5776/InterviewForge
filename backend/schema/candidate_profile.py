from pydantic import BaseModel,EmailStr
import uuid
from datetime import datetime
from typing import Optional , Any 

class CandidateProfileCreate(BaseModel):
    target_role: Optional[str] = None
    experience_level : Optional[str] = None
    skills: list[str]
    preferences: dict[str, Any]


class CandidateProfileUpdate(BaseModel) : 
    target_role: Optional[str] = None
    experience_level : Optional[str] = None
    skills: Optional[list[str]]=None
    preferences: Optional[dict[str,Any]]=None


class CandidateProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    target_role: str
    experience_level: str
    skills: list[str]
    preferences: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}