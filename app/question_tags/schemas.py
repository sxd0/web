from pydantic import BaseModel
from datetime import datetime

class QuestionTagBase(BaseModel):
    question_id: int
    tag_id: int


class QuestionTagCreate(BaseModel):
    post_id: int
    tag_id: int

class QuestionTagRead(QuestionTagCreate):
    id: int
    model_config = {"from_attributes": True}
