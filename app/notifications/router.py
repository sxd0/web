from fastapi import APIRouter
from app.notifications.schemas import NotificationsCreate, NotificationsRead
from app.notifications.dao import NotificationsDAO

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=list[NotificationsRead])
async def get_all():
    return await NotificationsDAO().find_all()

@router.post("/", response_model=NotificationsRead)
async def create(payload: NotificationsCreate):
    return await NotificationsDAO().add(**payload.dict())