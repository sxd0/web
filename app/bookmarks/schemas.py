from pydantic import BaseModel
from datetime import datetime

class BookmarkBase(BaseModel):
    post_id: int

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkRead(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }