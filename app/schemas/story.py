from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.prediction import PredictionResponse


class StoryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    category: str = Field(..., max_length=20)
    control_score: int = Field(..., ge=1, le=5)
    stress_score: int = Field(..., ge=1, le=5)
    satisfaction_score: int = Field(..., ge=1, le=5)


class StoryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    category: str
    control_score: int
    stress_score: int
    satisfaction_score: int
    views_count: int
    created_at: datetime
    prediction: Optional[PredictionResponse] = None

    model_config = {"from_attributes": True}


class StoryListItem(BaseModel):
    id: int
    user_id: int
    title: str
    category: str
    views_count: int
    created_at: datetime
    prediction: Optional[PredictionResponse] = None

    model_config = {"from_attributes": True}
