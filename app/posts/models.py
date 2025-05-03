from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from app.database import Base


class PostType(enum.Enum):
    question = 'question'
    answer = 'answer'

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    views = Column(Integer, default=0)
    is_closed = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    is_accepted = Column(Boolean, default=False)
    post_type = Column(Enum(PostType), nullable=False)
    vote_count = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey('posts.id'))

    author = relationship('User')
    parent = relationship('Post', remote_side=[id])

    def __str__(self):
        return self.name