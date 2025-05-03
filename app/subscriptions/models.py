from datetime import datetime, timezone
import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer
from app.database import Base
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import relationship



class SubscriptionType(enum.Enum):
    user = 'user'
    post = 'post'


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(Enum(SubscriptionType), nullable=False)
    targetuser_id = Column(Integer, ForeignKey('users.id'))
    targetpost_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="subscriptions", foreign_keys=[user_id])
    target_user = relationship("User", back_populates="target_subscriptions", foreign_keys=[targetuser_id])

