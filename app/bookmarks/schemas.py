from pydantic import BaseModel
from datetime import datetime

class BookmarkBase(BaseModel):
    post_id: int

class BookmarkCreate(BaseModel):
    post_id: int
    is_active: bool = True

class BookmarkRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}