from datetime import datetime
from jose import jwt, JWTError

from fastapi import Depends, HTTPException, Request, status
from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import User

def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")
    return token


def get_refresh_token(request: Request): 
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found token") #

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not expired")
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = await UsersDAO().find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

def require_role(role_id: int):
    async def _require_role(user: User = Depends(get_current_user)) -> User:
        if user.role_id != role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges"
            )
        return user
    return _require_role

async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.role_id != 1:
        raise HTTPException(status_code=403, detail="Admin only")
    return user
