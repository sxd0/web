from fastapi import APIRouter, Depends, HTTPException
from app.subscriptions.schemas import SubscriptionCreate, SubscriptionRead
from app.subscriptions.dao import SubscriptionsDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/subscriptions", tags=["Подписки"])

@router.get("/", response_model=list[SubscriptionRead])
async def get_subscriptions(user: User = Depends(get_current_user)):
    return await SubscriptionsDAO().find_all(user_id=user.id)

@router.post("/", response_model=SubscriptionRead)
async def create_subscription(payload: SubscriptionCreate, user: User = Depends(get_current_user)):
    if payload.type == "user" and not payload.targetuser_id:
        raise HTTPException(status_code=400, detail="targetuser_id is required for 'user' subscriptions")
    if payload.type == "post" and not payload.targetpost_id:
        raise HTTPException(status_code=400, detail="targetpost_id is required for 'post' subscriptions")
    return await SubscriptionsDAO().add(user_id=user.id, **payload.dict())


@router.delete("/{subscription_id}", response_model=dict)
async def delete_subscription(subscription_id: int, user: User = Depends(get_current_user)):
    sub = await SubscriptionsDAO().find_one_or_none(id=subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if sub.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await SubscriptionsDAO().delete_by_id(subscription_id)
    return {"status": "deleted"}