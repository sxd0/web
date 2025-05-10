from app.database import async_session_maker
from app.bookmarks.models import Bookmark
from app.users.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_bookmarks(user_id: int | None = None):
    async with async_session_maker() as session:
        stmt = select(Bookmark).options(
            selectinload(Bookmark.user),
            selectinload(Bookmark.post)
        )
        if user_id:
            stmt = stmt.where(Bookmark.user_id == user_id)
        stmt = stmt.order_by(Bookmark.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()
