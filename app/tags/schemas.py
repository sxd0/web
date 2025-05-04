from pydantic import BaseModel
from datetime import datetime

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: str | None = None

class TagRead(TagBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }