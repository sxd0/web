from pydantic import BaseModel
from datetime import datetime

class VoteBase(BaseModel):
    post_id: int
    value: int  # +1 или -1

class VoteCreate(BaseModel):
    post_id: int
    vote_type: str  # ENUM: up/down

class VoteRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    vote_type: str

    model_config = {"from_attributes": True}