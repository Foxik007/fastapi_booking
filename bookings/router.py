from fastapi import APIRouter
from sqlalchemy import select

from bookings.dao import BookingDAO
from bookings.models import Bookings
from database import async_session_maker

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование'],
)

@router.get('')
async def get_bookings():
    return await BookingDAO.find_all()