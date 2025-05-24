from sqlalchemy import delete
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.question_tags.models import QuestionTag

class QuestionTagsDAO(BaseDAO):
    def __init__(self):
        super().__init__(QuestionTag)

    async def delete_all_for_post(self, question_id: int):
        async with async_session_maker() as session:
            await session.execute(
                delete(QuestionTag).where(QuestionTag.question_id == question_id)
            )
            await session.commit()
