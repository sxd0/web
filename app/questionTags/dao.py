from app.dao.base import BaseDAO
from app.questionTags.models import QuestionTag

class UsersDAO(BaseDAO):
    def __init__(self):
        super().__init__(QuestionTag)
