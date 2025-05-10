from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.posts.dao import PostsDAO
from app.users.auth import authenticate_user, create_access_token, create_refresh_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_refresh_token
from app.users.models import User
from app.users.schemas import SUser, SUserLogin, SUserRegister, SUserUpdate
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
    user = await UsersDAO().find_one_or_none(id=int(user_id))
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


@router.get("/", response_model=list[SUser])
async def get_all_users(user: User = Depends(get_current_user)):
    if user.role_id != 2:
        raise HTTPException(status_code=403, detail="Admins only")
    return await UsersDAO().find_all()



@router.get("/{user_id}", response_model=SUser)
async def get_user_by_id(user_id: int, current: User = Depends(get_current_user)):
    if current.role_id != 2 and current.id != user_id:
        raise HTTPException(status_code=403, detail="Not permitted")
    user = await UsersDAO().find_one_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, payload: SUserUpdate, current: User = Depends(get_current_user)):
    if current.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot update others")

    data = payload.dict(exclude_none=True)
    data.pop("password", None)

    await UsersDAO().update(filter_by={"id": user_id}, **data)
    return {"status": "updated"}


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, current: User = Depends(get_current_user)):
    if current.id != user_id and current.role_id != 2:
        raise HTTPException(status_code=403, detail="Cannot delete others")

    posts = await PostsDAO().find_all(author_id=user_id)
    if posts:
        raise HTTPException(status_code=400, detail="User has posts and cannot be deleted")

    await UsersDAO().delete(id=user_id)
    return {"status": "deleted"}
