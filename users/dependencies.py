from datetime import datetime

from fastapi import Depends, HTTPException, Request
from jose import ExpiredSignatureError, JWTError, jwt

from config import settings
from exception import TokenExpired
from users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except HTTPException:
        raise TokenExpired
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=401)

    return user
