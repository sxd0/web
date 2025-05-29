from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from app.bookmarks.schemas import BookmarkCreate, BookmarkRead
from app.bookmarks.dao import BookmarksDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from sqlalchemy.orm import joinedload
from app.database import async_session_maker
from sqlalchemy import select
from app.bookmarks.models import Bookmark
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.dependencies import get_current_user


router = APIRouter(prefix="/bookmarks", tags=["Закладки"])

@router.get("/", response_model=list[BookmarkRead])
async def get_bookmarks(user: User = Depends(get_current_user)):
    return await BookmarksDAO().find_all(user_id=user.id)


@router.post("/", response_model=BookmarkRead)
async def create_bookmark(
    bookmark_in: BookmarkCreate = Body(...),
    session: AsyncSession = Depends(async_session_maker),
    user: User = Depends(get_current_user),
):

    stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.post_id == bookmark_in.post_id
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        if not existing.is_active:
            existing.is_active = True
            await session.commit()
            await session.refresh(existing)
            return existing
        else:
            raise HTTPException(status_code=409, detail="Bookmark already exists")

    new_bookmark = Bookmark(
        user_id=user.id,
        post_id=bookmark_in.post_id,
        is_active=True,
    )
    session.add(new_bookmark)
    await session.commit()
    await session.refresh(new_bookmark)
    return new_bookmark


@router.delete("/{post_id}", response_model=dict)
async def remove_bookmark(post_id: int, user: User = Depends(get_current_user)):
    bookmark = await BookmarksDAO().find_one_or_none(user_id=user.id, post_id=post_id)
    if not bookmark:
        return {"status": "already deleted"}

    await BookmarksDAO().delete(id=bookmark.id)
    return {"status": "bookmark deleted"}


@router.get("/my", response_model=list[BookmarkRead])
async def get_my_bookmarks(user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Bookmark)
            .options(joinedload(Bookmark.post))
            .where(Bookmark.user_id == user.id)
        )
        return result.scalars().all()


