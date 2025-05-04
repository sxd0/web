from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    type: str
    message: str

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }