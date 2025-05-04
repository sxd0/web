from pydantic import BaseModel
from datetime import datetime

class QuestionTagBase(BaseModel):
    post_id: int
    tag_id: int

class QuestionTagCreate(QuestionTagBase):
    pass

class QuestionTagRead(QuestionTagBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }