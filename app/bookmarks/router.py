from fastapi import APIRouter
from app.bookmarks.schemas import BookmarksCreate, BookmarksRead
from app.bookmarks.dao import BookmarksDAO

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

@router.get("/", response_model=list[BookmarksRead])
async def get_all():
    return await BookmarksDAO().find_all()

@router.post("/", response_model=BookmarksRead)
async def create(payload: BookmarksCreate):
    return await BookmarksDAO().add(**payload.dict())