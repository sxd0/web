from pydantic import BaseModel
from datetime import datetime

class SubscriptionBase(BaseModel):
    target_user_id: int

class SubscriptionCreate(BaseModel):
    type: str  # ENUM: user / post
    targetuser_id: int
    is_active: bool = True

class SubscriptionRead(BaseModel):
    id: int
    user_id: int
    type: str
    targetuser_id: int
    is_active: bool

    model_config = {"from_attributes": True}