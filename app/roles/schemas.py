from pydantic import BaseModel
from datetime import datetime

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }