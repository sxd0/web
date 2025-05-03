from pydantic import BaseModel
from datetime import datetime

class TagsBase(BaseModel):
    user_id: int

class TagsCreate(TagsBase):
    pass

class TagsRead(TagsBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }