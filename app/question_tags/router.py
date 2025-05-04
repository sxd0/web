from fastapi import APIRouter, Depends, HTTPException
from app.question_tags.schemas import QuestionTagCreate, QuestionTagRead
from app.question_tags.dao import QuestionTagsDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/question-tags", tags=["Связи: Пост ↔ Тег"])

@router.get("/", response_model=list[QuestionTagRead])
async def get_question_tags():
    return await QuestionTagsDAO().find_all()

@router.post("/", response_model=QuestionTagRead)
async def create_question_tag(payload: QuestionTagCreate, user: User = Depends(get_current_user)):
    return await QuestionTagsDAO().add(**payload.dict())

@router.delete("/{qt_id}", response_model=dict)
async def delete_question_tag(qt_id: int, user: User = Depends(get_current_user)):
    tag = await QuestionTagsDAO().find_one_or_none(id=qt_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Link not found")
    await QuestionTagsDAO().delete_by_id(qt_id)
    return {"status": "deleted"}