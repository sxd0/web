from pydantic import BaseModel, ConfigDict
from datetime import datetime

class QuestionTagBase(BaseModel):
    question_id: int
    tag_id: int

    model_config = ConfigDict(from_attributes=True)

class QuestionTagCreate(BaseModel):
    post_id: int
    tag_id: int

class QuestionTagRead(QuestionTagCreate):
    id: int
    model_config = {"from_attributes": True}
