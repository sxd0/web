from app.database import async_session_maker
from app.users.models import User
from app.roles.models import Role
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_users(role_id: int | None = None):
    async with async_session_maker() as session:
        stmt = select(User).options(selectinload(User.role))
        if role_id:
            stmt = stmt.where(User.role_id == role_id)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_user(user_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

async def get_all_roles():
    async with async_session_maker() as session:
        result = await session.execute(select(Role))
        return result.scalars().all()

async def update_user(user_id: int, email: str, role_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.email = email
            user.role_id = role_id
            await session.commit()
