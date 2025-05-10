from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class SUserBase(BaseModel):
    username: str
    email: EmailStr

class SUser(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    reputation: int
    is_visible: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True}

class SUserRegister(BaseModel):
    username: str
    email: str
    password: str

class SUserLogin(BaseModel):
    email: str
    password: str

class SUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
