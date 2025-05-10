from app.database import async_session_maker
from app.tags.models import Tag
from sqlalchemy import select

async def get_tags():
    async with async_session_maker() as session:
        result = await session.execute(select(Tag))
        return result.scalars().all()
