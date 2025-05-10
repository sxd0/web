from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationType(str, Enum):
    NewAnswer = "NewAnswer"
    NewQuestion = "NewQuestion"

class NotificationCreate(BaseModel):
    type: NotificationType
    message: str
    related_user_id: Optional[int] = None
    related_post_id: Optional[int] = None

class NotificationRead(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    message: str
    created_at: datetime
    related_user_id: Optional[int]
    related_post_id: Optional[int]

    model_config = {"from_attributes": True}
