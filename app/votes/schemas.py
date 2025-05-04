from pydantic import BaseModel
from datetime import datetime

class VoteBase(BaseModel):
    post_id: int
    value: int  # +1 или -1

class VoteCreate(VoteBase):
    pass

class VoteRead(VoteBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }