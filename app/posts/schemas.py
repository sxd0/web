from pydantic import BaseModel
from datetime import datetime

class PostsBase(BaseModel):
    user_id: int

class PostsCreate(PostsBase):
    pass

class PostsRead(PostsBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }