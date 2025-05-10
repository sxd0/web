from fastapi import APIRouter, Depends, HTTPException
from app.tags.schemas import TagCreate, TagUpdate, TagRead
from app.tags.dao import TagsDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/tags", tags=["Теги"])

@router.get("/", response_model=list[TagRead])
async def get_tags():
    return await TagsDAO().find_all()

@router.post("/", response_model=TagRead)
async def create_tag(payload: TagCreate, user: User = Depends(get_current_user)):
    return await TagsDAO().add(**payload.dict())

@router.put("/{tag_id}", response_model=dict)
async def update_tag(tag_id: int, payload: TagUpdate, user: User = Depends(get_current_user)):
    tag = await TagsDAO().find_one_or_none(id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await TagsDAO().update(filter_by={"id": tag_id}, **payload.dict(exclude_unset=True))
    return {"status": "updated"}

@router.delete("/{tag_id}", response_model=dict)
async def delete_tag(tag_id: int, user: User = Depends(get_current_user)):
    tag = await TagsDAO().find_one_or_none(id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await TagsDAO().delete(id=tag_id)
    return {"status": "deleted"}