from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from app.database import Base
from sqlalchemy.orm import relationship


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    user = relationship("User", backref="bookmarks")
    post = relationship("Post", backref="bookmarks")

    def __str__(self):
        return f"{self.user_id} → {self.post_id}"
