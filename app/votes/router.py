from fastapi import APIRouter, Depends, HTTPException
from app.votes.schemas import VoteCreate, VoteRead
from app.votes.dao import VotesDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/votes", tags=["Голоса"])

@router.get("/", response_model=list[VoteRead])
async def get_votes(user: User = Depends(get_current_user)):
    return await VotesDAO().find_all(user_id=user.id)

@router.post("/", response_model=VoteRead)
async def create_vote(payload: VoteCreate, user: User = Depends(get_current_user)):
    existing = await VotesDAO().find_one_or_none(user_id=user.id, post_id=payload.post_id)
    if existing:
        raise HTTPException(status_code=400, detail="Already voted")
    return await VotesDAO().add(user_id=user.id, post_id=payload.post_id, vote_type=payload.vote_type)

@router.delete("/{vote_id}", response_model=dict)
async def delete_vote(vote_id: int, user: User = Depends(get_current_user)):
    vote = await VotesDAO().find_one_or_none(id=vote_id)
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    if vote.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await VotesDAO().delete_by_id(vote_id)
    return {"status": "deleted"}