from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class VoteCreate(BaseModel):
    story_id: int
    user_id: int
    vote_type: Literal["+", "-"]


class VoteResponse(BaseModel):
    id: int
    story_id: int
    user_id: int
    vote_type: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VoteSummary(BaseModel):
    story_id: int
    plus_count: int
    minus_count: int
    total_count: int
