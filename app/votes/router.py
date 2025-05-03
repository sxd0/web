from fastapi import APIRouter
from app.votes.schemas import VotesCreate, VotesRead
from app.votes.dao import VotesDAO

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.get("/", response_model=list[VotesRead])
async def get_all():
    return await VotesDAO().find_all()

@router.post("/", response_model=VotesRead)
async def create(payload: VotesCreate):
    return await VotesDAO().add(**payload.dict())