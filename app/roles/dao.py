from app.dao.base import BaseDAO
from app.roles.models import Role

class RolesDAO(BaseDAO):
    def __init__(self):
        super().__init__(Role)
