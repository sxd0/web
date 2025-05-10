from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class VoteType(str, Enum):
    up = "up"
    down = "down"

class VoteCreate(BaseModel):
    post_id: int
    vote_type: VoteType

class VoteRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    vote_type: VoteType

    model_config = {"from_attributes": True}

