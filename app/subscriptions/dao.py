from app.dao.base import BaseDAO
from app.subscriptions.models import Subscription

class SubscriptionsDAO(BaseDAO):
    def __init__(self):
        super().__init__(Subscription)
