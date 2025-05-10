from app.database import async_session_maker
from app.votes.models import Vote
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_votes():
    async with async_session_maker() as session:
        stmt = select(Vote).options(
            selectinload(Vote.user),
            selectinload(Vote.post)
        )

        result = await session.execute(stmt)
        return result.scalars().all()
