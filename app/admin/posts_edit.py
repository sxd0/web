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
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalar_one_or_none()
        if not post:
            return False
        for key, value in data.items():
            setattr(post, key, value)
        post.updated_at = datetime.utcnow()
        await session.commit()
        return True
