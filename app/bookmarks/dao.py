from sqlalchemy import select
from app.bookmarks.models import Bookmark
from app.dao.base import BaseDAO

class BookmarksDAO(BaseDAO):
    def __init__(self):
        super().__init__(Bookmark)

    async def get_by_user(self, user_id: int) -> list[Bookmark]:
        async with self.session_factory() as session:
            stmt = select(Bookmark).where(
                Bookmark.user_id == user_id,
                Bookmark.is_active.is_(True)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
