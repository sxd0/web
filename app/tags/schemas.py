from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TagBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TagCreate(BaseModel):
    name: str
    description: str

class TagRead(TagCreate):
    id: int

    model_config = {"from_attributes": True}
