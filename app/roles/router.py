from fastapi import APIRouter
from app.roles.schemas import RolesCreate, RolesRead
from app.roles.dao import RolesDAO

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RolesRead])
async def get_all():
    return await RolesDAO().find_all()

@router.post("/", response_model=RolesRead)
async def create(payload: RolesCreate):
    return await RolesDAO().add(**payload.dict())