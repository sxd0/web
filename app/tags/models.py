from sqlalchemy import Column, Integer, String
from app.database import Base




class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    def __str__(self):
        return self.name