from datetime import date

from fastapi import APIRouter, Depends, Request
from pydantic import TypeAdapter, parse_obj_as
from sqlalchemy import select

from bookings.dao import BookingDAO
from bookings.models import Bookings
from bookings.schemas import SBooking, SNewBooking
from database import async_session_maker
from tasks.tasks import send_booking_confirmation_email
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
    booking = await BookingDAO.add(user.id,room_id,date_from,date_to)

    # TypeAdapter и model_dump - это новинки версии Pydantic 2.0
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    # Celery - отдельная библиотека
    send_booking_confirmation_email.delay(booking, user.email)
    # Background Tasks - встроено в FastAPI
    # background_tasks.add_task(send_booking_confirmation_email, booking, user.email)
    return booking



@router.delete('/delete')
async def delete_booking(booking_id:int,user:Users = Depends(get_current_user)):
    await BookingDAO.delete(user_id=user.id,id=booking_id)