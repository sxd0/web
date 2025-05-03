from app.dao.base import BaseDAO
from app.bookmarks.models import Bookmark

class BookmarksDAO(BaseDAO):
    def __init__(self):
        super().__init__(Bookmark)
