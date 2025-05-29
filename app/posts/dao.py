from sqlalchemy import func, select
from app.dao.base import BaseDAO
from app.posts.models import Post, PostType
from app.database import async_session_maker

class PostsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Post)

    async def search_by_text(self, query: str) -> list[Post]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Post).where(Post.title.ilike(f"%{query}%"))
            )
            return result.scalars().all()



    async def count_answers(self, question_id: int) -> int:
        async with async_session_maker() as session:
            result = await session.execute(
                select(func.count()).where(Post.parent_id == question_id, Post.post_type == PostType.answer)
            )
            return result.scalar()