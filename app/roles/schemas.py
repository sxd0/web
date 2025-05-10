from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RoleBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class RoleCreate(BaseModel):
    name: str

class RoleRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

class RoleUpdate(BaseModel):
    name: Optional[str] = None