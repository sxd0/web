from sqlalchemy import select
from app.dao.base import BaseDAO
from app.subscriptions.models import Subscription

class SubscriptionsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Subscription)

    async def get_subscriptions(self, user_id: int) -> list[Subscription]:
        async with self.session_factory() as session:
            stmt = select(Subscription).where(
                Subscription.subscriber_id == user_id
            )
            result = await session.execute(stmt)
            return result.scalars().all()
