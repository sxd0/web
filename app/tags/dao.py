from app.dao.base import BaseDAO
from app.tags.models import Tag

class TagsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Tag)
