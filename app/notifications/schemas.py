from pydantic import BaseModel
from datetime import datetime

class NotificationsBase(BaseModel):
    user_id: int

class NotificationsCreate(NotificationsBase):
    pass

class NotificationsRead(NotificationsBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }