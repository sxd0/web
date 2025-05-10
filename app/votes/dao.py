from sqlalchemy import select
from app.dao.base import BaseDAO
from app.votes.models import Vote

class VotesDAO(BaseDAO):
    def __init__(self):
        super().__init__(Vote)

    async def get_user_vote(self, user_id: int, post_id: int) -> Vote | None:
        async with self.session_factory() as session:
            stmt = select(Vote).where(
                Vote.user_id == user_id,
                Vote.post_id == post_id
            )
            result = await session.execute(stmt)
            return result.scalars().first()
