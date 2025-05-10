from app.database import async_session_maker
from app.posts.models import Post
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import datetime

async def get_posts(
    search: str | None = None,
    is_closed: bool | None = None,
    is_visible: bool | None = None,
    post_type: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None
) -> list[Post]:
    async with async_session_maker() as session:
        stmt = select(Post).options(selectinload(Post.author))
        conditions = []

        if search:
            conditions.append(
                Post.title.ilike(f"%{search}%") | Post.body.ilike(f"%{search}%")
            )
        if is_closed is not None:
            conditions.append(Post.is_closed == is_closed)
        if is_visible is not None:
            conditions.append(Post.is_visible == is_visible)
        if post_type:
            conditions.append(Post.post_type == post_type)
        if created_from:
            try:
                from_dt = datetime.fromisoformat(created_from)
                conditions.append(Post.created_at >= from_dt)
            except ValueError:
                pass
        if created_to:
            try:
                to_dt = datetime.fromisoformat(created_to)
                conditions.append(Post.created_at <= to_dt)
            except ValueError:
                pass

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(Post.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()
