from pydantic import BaseModel, EmailStr
from datetime import datetime

class SUserBase(BaseModel):
    username: str
    email: EmailStr

# class SUserRegister(SUserBase):
#     password: str

class SUserLogin(BaseModel):
    email: EmailStr
    password: str

class SUserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

class SUser(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    reputation: int
    is_visible: bool

    model_config = {
        "from_attributes": True
    }

class SUserRegister(BaseModel):
    username: str
    email: str
    password: str