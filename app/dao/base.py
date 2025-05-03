from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker
import logging

logger = logging.getLogger(__name__)


class BaseDAO:
    def __init__(self, model):
        self.model = model

    async def find_one_or_none(self, **filter_by):
        async with async_session_maker() as session:
            try:
                query = select(self.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalars().one_or_none()
            except SQLAlchemyError as e:
                logger.error(f"Error in find_one_or_none: {e}")
                raise

    async def find_all(self, offset: int = 0, limit: int = 100, **filter_by):
        async with async_session_maker() as session:
            try:
                query = select(self.model).filter_by(**filter_by).offset(offset).limit(limit)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                logger.error(f"Error in find_all: {e}")
                raise

    async def add(self, **data):
        async with async_session_maker() as session:
            try:
                obj = self.model(**data)
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except SQLAlchemyError as e:
                logger.error(f"Error in add: {e}")
                raise

    async def delete(self, **filter_by):
        async with async_session_maker() as session:
            try:
                query = delete(self.model).filter_by(**filter_by)
                await session.execute(query)
                await session.commit()
            except SQLAlchemyError as e:
                logger.error(f"Error in delete: {e}")
                raise

    async def update(self, filter_by: dict, **data):
        async with async_session_maker() as session:
            try:
                query = update(self.model).filter_by(**filter_by).values(**data).returning(self.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalars().all()
            except SQLAlchemyError as e:
                logger.error(f"Error in update: {e}")
                raise

    async def find_all_for_list(self, field_name: str, values: list):
        if not hasattr(self.model, field_name):
            raise ValueError(f"Field {field_name} does not exist in model {self.model.__name__}")
        async with async_session_maker() as session:
            try:
                column = getattr(self.model, field_name)
                query = select(self.model).filter(column.in_(values))
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                logger.error(f"Error in find_all_for_list: {e}")
                raise
