from datetime import datetime
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    id: int
    story_id: int
    luck_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=1)
    model_version: str
    created_at: datetime

    model_config = {"from_attributes": True, "protected_namespaces": ()}
