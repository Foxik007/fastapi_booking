from sqlalchemy import select

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings
