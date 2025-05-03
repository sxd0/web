from datetime import datetime, timezone
import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text
from app.database import Base
from sqlalchemy.dialects.postgresql import ENUM as PGEnum



class NotificationType(enum.Enum):
    NewAnswer = 'NewAnswer'
    NewQuestion = 'NewQuestion'


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(Enum(NotificationType), nullable=False)
    relatedpost_id = Column(Integer, ForeignKey('posts.id'))
    relateduser_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

