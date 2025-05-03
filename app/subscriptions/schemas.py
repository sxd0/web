from pydantic import BaseModel
from datetime import datetime

class SubscriptionsBase(BaseModel):
    user_id: int

class SubscriptionsCreate(SubscriptionsBase):
    pass

class SubscriptionsRead(SubscriptionsBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }