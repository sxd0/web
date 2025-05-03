from pydantic import BaseModel
from datetime import datetime

class VotesBase(BaseModel):
    user_id: int

class VotesCreate(VotesBase):
    pass

class VotesRead(VotesBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }