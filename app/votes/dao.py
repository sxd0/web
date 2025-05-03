from app.dao.base import BaseDAO
from app.votes.models import Vote

class VotesDAO(BaseDAO):
    def __init__(self):
        super().__init__(Vote)
