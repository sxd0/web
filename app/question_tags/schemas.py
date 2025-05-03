from pydantic import BaseModel
from datetime import datetime

class QuestionTagsBase(BaseModel):
    user_id: int

class QuestionTagsCreate(QuestionTagsBase):
    pass

class QuestionTagsRead(QuestionTagsBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }