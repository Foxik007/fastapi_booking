from datetime import date

from fastapi import APIRouter, Request, Depends
from sqlalchemy import select

from bookings.dao import BookingDAO
from bookings.models import Bookings
from bookings.schemas import SBooking
from database import async_session_maker
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование'],
)

#Получаем список всех броней залогиненного пользователя
@router.get('')
async def get_bookings(user:Users = Depends(get_current_user)):
    return await BookingDAO.find_by_user(user.id)

@router.post('/add')
async def add_booking(
        room_id:int, date_from: date, date_to: date,
        user:Users = Depends(get_current_user),
):
    await BookingDAO.add(user.id,room_id,date_from,date_to)


@router.delete('/{booking_id}')
async def delete_booking(booking_id:int,user:Users = Depends(get_current_user)):
    await BookingDAO.delete(user_id=user.id,id=booking_id)