from fastapi import APIRouter
from app.tags.schemas import TagsCreate, TagsRead
from app.tags.dao import TagsDAO

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=list[TagsRead])
async def get_all():
    return await TagsDAO().find_all()

@router.post("/", response_model=TagsRead)
async def create(payload: TagsCreate):
    return await TagsDAO().add(**payload.dict())