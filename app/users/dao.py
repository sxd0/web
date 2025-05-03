from sqlalchemy import delete, update
from app.dao.base import BaseDAO
from app.users.models import User
from app.database import async_session_maker



class UsersDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    async def update(self, user_id: int, data: dict):
        async with async_session_maker() as session:
            await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(**data)
            )
            await session.commit()

    async def delete(self, user_id: int):
        async with async_session_maker() as session:
            await session.execute(
                delete(User).where(User.id == user_id)
            )
            await session.commit()