from sqlalchemy import select
from app.dao.base import BaseDAO
from app.posts.models import Post

class PostsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Post)

    async def search_by_text(self, query: str) -> list[Post]:
        async with self.session_factory() as session:
            stmt = select(Post).where(
                Post.body.ilike(f"%{query}%") | Post.title.ilike(f"%{query}%")
            )
            result = await session.execute(stmt)
            return result.scalars().all()
