
from fastapi import APIRouter, Depends, Response
from fastapi_cache.decorator import cache

from exception import UserAlreadyExistsException
from users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.models import Users
from users.shemas import SUserAuth

router = APIRouter(
    prefix='/auth',
    tags= ['Auth & Пользователи']
)


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post('/logout')
async def logout_user(responce:Response):
    responce.delete_cookie('booking_access_token')
    return 'Пользователь вышел'

@router.get('/me')
async def read_user_me(current_user:Users = Depends(get_current_user)):
    return current_user


@router.get('/all')
async def all_users():
    return await UsersDAO.find_all()

