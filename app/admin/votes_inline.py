from app.database import async_session_maker
from app.votes.models import Vote
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_votes_for_post(post_id: int):
    async with async_session_maker() as session:
        stmt = (
            select(Vote)
            .where(Vote.post_id == post_id)
            .options(selectinload(Vote.user))
            .order_by(Vote.created_at.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()
