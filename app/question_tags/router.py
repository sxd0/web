from fastapi import APIRouter, Depends, HTTPException
from app.question_tags.schemas import QuestionTagCreate, QuestionTagRead
from app.question_tags.dao import QuestionTagsDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.posts.dao import PostsDAO
from app.posts.schemas import PostType

router = APIRouter(prefix="/question-tags", tags=["Привязка тегов"])

@router.get("/", response_model=list[QuestionTagRead])
async def get_all_links():
    return await QuestionTagsDAO().find_all()


@router.post("/", response_model=QuestionTagRead)
async def create_link(payload: QuestionTagCreate, user: User = Depends(get_current_user)):
    question = await PostsDAO().find_one_or_none(id=payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question.post_type != PostType.question:
        raise HTTPException(status_code=400, detail="Only questions can be tagged")

    return await QuestionTagsDAO().add(**payload.dict())


@router.put("/{link_id}", response_model=QuestionTagRead)
async def update_link(link_id: int, payload: QuestionTagCreate):
    await QuestionTagsDAO().update(filter_by={"id": link_id}, **payload.dict())
    return await QuestionTagsDAO().find_one_or_none(id=link_id)


@router.delete("/{link_id}", response_model=dict)
async def delete_link(link_id: int):
    existing = await QuestionTagsDAO().find_one_or_none(id=link_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Link not found")
    await QuestionTagsDAO().delete(id=link_id)
    return {"status": "deleted"}
