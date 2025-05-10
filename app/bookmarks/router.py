from fastapi import APIRouter, Depends, HTTPException
from app.bookmarks.schemas import BookmarkCreate, BookmarkRead
from app.bookmarks.dao import BookmarksDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/bookmarks", tags=["Закладки"])

@router.get("/", response_model=list[BookmarkRead])
async def get_bookmarks(user: User = Depends(get_current_user)):
    return await BookmarksDAO().find_all(user_id=user.id)


@router.post("/", response_model=BookmarkRead)
async def create_bookmark(payload: BookmarkCreate, user: User = Depends(get_current_user)):
    existing = await BookmarksDAO().find_one_or_none(user_id=user.id, post_id=payload.post_id)
    if existing:
        raise HTTPException(status_code=409, detail="Bookmark already exists")

    return await BookmarksDAO().add(user_id=user.id, **payload.dict())


@router.delete("/{post_id}", response_model=dict)
async def remove_bookmark(post_id: int, user: User = Depends(get_current_user)):
    bookmark = await BookmarksDAO().find_one_or_none(user_id=user.id, post_id=post_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await BookmarksDAO().delete(id=bookmark.id)
    return {"status": "bookmark deleted"}


@router.get("/my", response_model=list[BookmarkRead])
async def get_my_bookmarks(user: User = Depends(get_current_user)):
    return await BookmarksDAO().find_all(user_id=user.id)


@router.get("/bookmarks/my", response_model=list[BookmarkRead])
async def my_bookmarks(user: User = Depends(get_current_user)):
    return await BookmarksDAO().get_by_user(user.id)
