from app.dao.base import BaseDAO
from app.notifications.models import Notification

class UsersDAO(BaseDAO):
    def __init__(self):
        super().__init__(Notification)
