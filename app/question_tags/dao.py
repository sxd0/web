from app.dao.base import BaseDAO
from app.question_tags.models import QuestionTag

class QuestionTagsDAO(BaseDAO):
    def __init__(self):
        super().__init__(QuestionTag)
