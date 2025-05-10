from sqlalchemy import select
from app.dao.base import BaseDAO
from app.notifications.models import Notification

class NotificationsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Notification)

    async def get_recent_for_user(self, user_id: int, limit: int = 10) -> list[Notification]:
        async with self.session_factory() as session:
            stmt = select(Notification).where(
                Notification.user_id == user_id
            ).order_by(Notification.created_at.desc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()
