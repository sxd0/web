from pydantic import BaseModel
from datetime import datetime

class SubscriptionBase(BaseModel):
    target_user_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionRead(SubscriptionBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }