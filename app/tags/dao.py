from sqlalchemy import select
from app.dao.base import BaseDAO
from app.tags.models import Tag
from app.database import async_session_maker

class TagsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Tag)

    async def get_or_create(self, name: str) -> Tag:
        async with async_session_maker() as session:
            result = await session.execute(select(Tag).where(Tag.name == name))
            tag = result.scalars().first()
            if tag:
                return tag
            new_tag = Tag(name=name)
            session.add(new_tag)
            await session.commit()
            await session.refresh(new_tag)
            return new_tag
