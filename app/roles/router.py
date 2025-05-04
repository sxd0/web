from fastapi import APIRouter, Depends, HTTPException
from app.roles.dao import RolesDAO
from app.roles.schemas import RoleCreate, RoleRead
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/roles", tags=["Роли"])

@router.get("/", response_model=list[RoleRead])
async def get_roles():
    return await RolesDAO().find_all()

@router.get("/{role_id}", response_model=RoleRead)
async def get_role(role_id: int):
    role = await RolesDAO().find_one_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/", response_model=RoleRead)
async def create_role(payload: RoleCreate, user: User = Depends(get_current_user)):
    return await RolesDAO().add(**payload.dict())

@router.put("/{role_id}", response_model=dict)
async def update_role(role_id: int, payload: RoleCreate, user: User = Depends(get_current_user)):
    role = await RolesDAO().find_one_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await RolesDAO().update_by_id(role_id, payload.dict())
    return {"status": "updated"}

@router.delete("/{role_id}", response_model=dict)
async def delete_role(role_id: int, user: User = Depends(get_current_user)):
    role = await RolesDAO().find_one_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await RolesDAO().delete_by_id(role_id)
    return {"status": "deleted"}