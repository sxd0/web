from app.database import async_session_maker
from app.roles.models import Role
from app.users.models import User
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

async def get_roles():
    async with async_session_maker() as session:
        stmt = select(Role).options(selectinload(Role.users))
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_role(role_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

async def count_users_for_role(role_id: int) -> int:
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.count()).select_from(User).where(User.role_id == role_id)
        )
        return result.scalar_one()

async def update_role(role_id: int, name: str):
    async with async_session_maker() as session:
        result = await session.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if role:
            role.name = name
            await session.commit()
