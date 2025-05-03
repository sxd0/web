from fastapi import APIRouter
from app.posts.schemas import PostsCreate, PostsRead
from app.posts.dao import PostsDAO

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[PostsRead])
async def get_all():
    return await PostsDAO().find_all()

@router.post("/", response_model=PostsRead)
async def create(payload: PostsCreate):
    return await PostsDAO().add(**payload.dict())