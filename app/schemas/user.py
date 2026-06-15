from datetime import datetime
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    grade: int = Field(..., ge=1, le=3)


class UserResponse(BaseModel):
    id: int
    nickname: str
    grade: int
    created_at: datetime

    model_config = {"from_attributes": True}
