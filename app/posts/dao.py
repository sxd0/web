from app.dao.base import BaseDAO
from app.posts.models import Post

class PostsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Post)
