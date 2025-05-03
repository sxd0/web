from app.dao.base import BaseDAO
from app.tags.models import Tag

class UsersDAO(BaseDAO):
    def __init__(self):
        super().__init__(Tag)
