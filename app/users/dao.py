from app.dao.base import BaseDAO
from app.users.models import User

class UsersDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)
