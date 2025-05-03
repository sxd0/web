from app.dao.base import BaseDAO
from app.notifications.models import Notification

class NotificationsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Notification)
