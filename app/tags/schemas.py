from pydantic import BaseModel
from datetime import datetime

class TagBase(BaseModel):
    name: str

class TagUpdate(BaseModel):
    name: str | None = None

class TagRead(BaseModel):
    id: int
    name: str
    description: str

    model_config = {"from_attributes": True}

class TagCreate(BaseModel):
    name: str
    description: str