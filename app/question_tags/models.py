from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer
from app.database import Base


class QuestionTag(Base):
    __tablename__ = 'question_tags'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete="CASCADE"), nullable=False)

    question = relationship('Post')
    tag = relationship('Tag')

    def __str__(self):
        return f"Tag #{self.tag_id} for Question #{self.question_id}"
