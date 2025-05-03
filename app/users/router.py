from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.users.auth import authenticate_user, create_access_token, create_refresh_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_refresh_token
from app.users.models import User
from app.users.schemas import SUser, SUserLogin, SUserRegister
from app.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserRegister):
    """Регистрация"""
    existing_user = await UsersDAO().find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User exists")
    hashed_password = get_password_hash(user_data.password)

    user = await UsersDAO().add(email=user_data.email, hashed_password=hashed_password, username=user_data.username)
    return user


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin) -> SUser:
    """Вход в свой аккаунт"""
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie("access_token", access_token,
                        httponly=True, secure=True, samesite="lax")
    response.set_cookie("refresh_token", refresh_token,
                        httponly=True, secure=True, samesite="lax")

    return user


@router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Depends(get_refresh_token)):
    """Перезагрузить токен"""
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True,
                        secure=True, samesite='lax')  # Возможно 'Strict'

    new_refresh_token = create_refresh_token({"sub": str(user.id)})
    response.set_cookie("refresh_token", new_refresh_token,
                        httponly=True, secure=True, samesite='lax')

    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    """Выход | Удаление куков"""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> SUser:
    """Вывод информации о себе"""
    return current_user
