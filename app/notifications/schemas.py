from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    type: str
    message: str

class NotificationCreate(BaseModel):
    type: str  # ENUM: NewAnswer / NewQuestion
    message: str

class NotificationRead(BaseModel):
    id: int
    user_id: int
    type: str
    message: str

    model_config = {"from_attributes": True}