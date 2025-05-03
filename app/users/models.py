from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.database import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=1)
    reputation = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_visible = Column(Boolean, default=True)

    role = relationship('Role', back_populates="users")

    subscriptions = relationship('Subscription', back_populates="user", foreign_keys="Subscription.user_id")
    target_subscriptions = relationship('Subscription', back_populates="target_user", foreign_keys="Subscription.targetuser_id")


