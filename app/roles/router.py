from fastapi import APIRouter, Depends, HTTPException
from app.roles.dao import RolesDAO
from app.roles.schemas import RoleCreate, RoleRead, RoleUpdate
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/roles", tags=["Роли"])

@router.get("/", response_model=list[RoleRead])
async def get_roles():
    """Получение всех ролей."""
    return await RolesDAO().find_all()

@router.get("/{role_id}", response_model=RoleRead)
async def get_role(role_id: int):
    """Получение роли по ID."""
    role = await RolesDAO().find_one_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/", response_model=RoleRead)
async def create_role(role_data: RoleCreate):
    """Создание новой роли."""
    return await RolesDAO().add(**role_data.dict())

@router.put("/{role_id}", response_model=dict)
async def update_role(role_id: int, data: RoleUpdate, user: User = Depends(get_current_user)):
    role = await RolesDAO().find_one_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await RolesDAO().update(filter_by={"id": role_id}, **data.dict(exclude_unset=True))
    return {"status": "updated"}

@router.delete("/{role_id}", response_model=dict)
async def delete_role(role_id: int, user: User = Depends(get_current_user)):
    role = await RolesDAO().find_one_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await RolesDAO().delete(id=role_id)
    return {"status": "deleted"}