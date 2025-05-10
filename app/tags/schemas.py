from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TagBase(BaseModel):
    name: str

class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TagCreate(BaseModel):
    name: str
    description: str

class TagRead(TagCreate):
    id: int

    model_config = {"from_attributes": True}
