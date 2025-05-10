from app.database import async_session_maker
from app.subscriptions.models import Subscription
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_user_subscriptions(user_id: int):
    async with async_session_maker() as session:
        stmt = (
            select(Subscription)
            .where(Subscription.user_id == user_id)
            .options(selectinload(Subscription.target_user))
            .order_by(Subscription.created_at.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()
