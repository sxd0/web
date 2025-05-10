from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class SubscriptionType(str, Enum):
    user = "user"
    post = "post"

class SubscriptionCreate(BaseModel):
    type: SubscriptionType
    targetuser_id: int | None = None
    targetpost_id: int | None = None
    is_active: bool = True


class SubscriptionRead(BaseModel):
    id: int
    user_id: int
    type: SubscriptionType
    targetuser_id: int | None = None
    targetpost_id: int | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
