from app.database import async_session_maker
from app.posts.models import Post
from sqlalchemy import select, update
from datetime import datetime

async def get_post_by_id(post_id: int) -> Post | None:
    async with async_session_maker() as session:
        result = await session.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

async def update_post_data(post_id: int, data: dict) -> bool:
    async with async_session_maker() as session:
        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(**data, updated_at=datetime.utcnow())
        )
        await session.execute(stmt)
        await session.commit()
        return True
