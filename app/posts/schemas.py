from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator, root_validator
from datetime import datetime

from app.posts.models import PostType

class PostBase(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    title: str
    body: str
    post_type: PostType
    parent_id: Optional[int] = None

    @model_validator(mode="after")
    def check_parent_id(self) -> "PostCreate":
        if self.post_type == PostType.question and self.parent_id is not None:
            raise ValueError("Questions must not have a parent_id.")
        if self.post_type == PostType.answer and self.parent_id is None:
            raise ValueError("Answers must have a parent_id.")
        return self

class PostRead(BaseModel):
    id: int
    title: str
    body: str
    post_type: str
    author_id: int
    is_closed: bool
    is_visible: bool
    is_accepted: bool
    created_at: datetime
    updated_at: datetime
    views: int
    vote_count: int
    parent_id: int | None = None

    model_config = {"from_attributes": True}


class PostReadDetailed(PostRead):
    tags: list[int] = []
    votes: int = 0


class PostReadWithTags(PostRead):
    tags: list[int]

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    is_closed: Optional[bool] = None
    is_visible: Optional[bool] = None
    is_accepted: Optional[bool] = None