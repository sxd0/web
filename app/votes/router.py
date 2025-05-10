from fastapi import APIRouter, Depends, HTTPException
from app.votes.schemas import VoteCreate, VoteRead
from app.votes.dao import VotesDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/votes", tags=["Голоса"])

@router.get("/", response_model=list[VoteRead])
async def get_all_votes():
    return await VotesDAO().find_all()


@router.post("/", response_model=VoteRead)
async def create_vote(payload: VoteCreate, user: User = Depends(get_current_user)):
    existing = await VotesDAO().find_one_or_none(user_id=user.id, post_id=payload.post_id)
    if existing:
        raise HTTPException(status_code=409, detail="User already voted for this post")

    return await VotesDAO().add(user_id=user.id, **payload.dict())


@router.delete("/", response_model=dict)
async def remove_vote(payload: VoteCreate, user: User = Depends(get_current_user)):
    existing = await VotesDAO().find_one_or_none(user_id=user.id, post_id=payload.post_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Vote not found")

    await VotesDAO().delete(id=existing.id)
    return {"status": "vote deleted"}


@router.get("/votes/my/{post_id}", response_model=VoteRead | None)
async def get_my_vote(post_id: int, user: User = Depends(get_current_user)):
    return await VotesDAO().get_user_vote(user.id, post_id)
