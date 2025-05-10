from fastapi import APIRouter, Depends, HTTPException
from app.notifications.schemas import NotificationCreate, NotificationRead
from app.notifications.dao import NotificationsDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/notifications", tags=["Уведомления"])

@router.get("/", response_model=list[NotificationRead])
async def get_notifications(user: User = Depends(get_current_user)):
    return await NotificationsDAO().find_all(user_id=user.id)

@router.post("/", response_model=NotificationRead)
async def create_notification(payload: NotificationCreate, user: User = Depends(get_current_user)):
    return await NotificationsDAO().add(user_id=user.id, **payload.dict())

@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(notification_id: int, user: User = Depends(get_current_user)):
    notification = await NotificationsDAO().find_one_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await NotificationsDAO().delete_by_id(notification_id)
    return {"status": "deleted"}


@router.get("/my", response_model=list[NotificationRead])
async def get_my_notifications(user: User = Depends(get_current_user)):
    return await NotificationsDAO().find_all(user_id=user.id)


@router.get("/notifications", response_model=list[NotificationRead])
async def get_notifications(user: User = Depends(get_current_user)):
    return await NotificationsDAO().get_recent_for_user(user.id)
