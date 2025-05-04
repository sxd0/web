from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: str | None = None

class PostRead(PostBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class PostReadWithTags(PostRead):
    tags: list[int]

class PostReadDetailed(PostBase):
    id: int
    user_id: int
    created_at: datetime
    tags: list[int] = []
    votes: int = 0
    
    model_config = {
        "from_attributes": True
    }