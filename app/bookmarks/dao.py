from sqlalchemy import select
from app.bookmarks.models import Bookmark
from app.dao.base import BaseDAO
from app.database import async_session_maker

class BookmarksDAO(BaseDAO):
    def __init__(self):
        super().__init__(Bookmark)

    async def get_by_user(self, user_id: int) -> list[Bookmark]:
        async with async_session_maker() as session:
            stmt = select(Bookmark).where(
                Bookmark.user_id == user_id,
                Bookmark.is_active.is_(True)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete(self, id: int) -> None:
        async with async_session_maker() as session:
            bookmark = await session.get(Bookmark, id)
            if bookmark:
                bookmark.is_active = False
                await session.commit()
