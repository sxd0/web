from pydantic import BaseModel
from datetime import datetime

class BookmarksBase(BaseModel):
    user_id: int

class BookmarksCreate(BookmarksBase):
    pass

class BookmarksRead(BookmarksBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }