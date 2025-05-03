from app.dao.base import BaseDAO
from app.subscriptions.models import Subscription

class UsersDAO(BaseDAO):
    def __init__(self):
        super().__init__(Subscription)
