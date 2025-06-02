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
        
    async def get_open_posts(self) -> list[Post]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Post).where(~Post.is_closed)
            )
            return result.scalars().all()

    async def get_recent_posts(self, limit: int = 10) -> list[Post]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Post).order_by(Post.created_at.desc()).limit(limit)
            )
            return result.scalars().all()

    async def get_average_views(self) -> float:
        async with async_session_maker() as session:
            result = await session.execute(select(func.avg(Post.views)))
            return result.scalar()

    async def get_max_votes(self) -> int:
        async with async_session_maker() as session:
            result = await session.execute(select(func.max(Post.vote_count)))
            return result.scalar()
