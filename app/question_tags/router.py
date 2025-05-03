from fastapi import APIRouter
from app.question_tags.schemas import QuestionTagsCreate, QuestionTagsRead
from app.question_tags.dao import QuestionTagsDAO

router = APIRouter(prefix="/question_tags", tags=["QuestionTags"])

@router.get("/", response_model=list[QuestionTagsRead])
async def get_all():
    return await QuestionTagsDAO().find_all()

@router.post("/", response_model=QuestionTagsRead)
async def create(payload: QuestionTagsCreate):
    return await QuestionTagsDAO().add(**payload.dict())