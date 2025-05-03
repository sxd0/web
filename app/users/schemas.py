from pydantic import BaseModel, EmailStr
from datetime import datetime

class SUserBase(BaseModel):
    username: str
    email: EmailStr

class SUserRegister(SUserBase):
    password: str

class SUserLogin(BaseModel):
    email: EmailStr
    password: str

class SUserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

class SUser(SUserBase):
    id: int
    role_id: int
    reputation: int
    created_at: datetime
    last_login: datetime | None
    is_visible: bool

    model_config = {
        "from_attributes": True
    }