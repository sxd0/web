from fastapi import APIRouter
from app.subscriptions.schemas import SubscriptionsCreate, SubscriptionsRead
from app.subscriptions.dao import SubscriptionsDAO

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.get("/", response_model=list[SubscriptionsRead])
async def get_all():
    return await SubscriptionsDAO().find_all()

@router.post("/", response_model=SubscriptionsRead)
async def create(payload: SubscriptionsCreate):
    return await SubscriptionsDAO().add(**payload.dict())