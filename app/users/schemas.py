from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str


    model_config = ConfigDict(from_attributes=True)


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

    
class SUser(BaseModel):
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
