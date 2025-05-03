from sqlalchemy.orm import relationship

import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer

from app.database import Base


class VoteType(enum.Enum):
    up = 'up'
    down = 'down'

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False)

    user = relationship('User')
    post = relationship('Post')

    def __str__(self):
        return self.name