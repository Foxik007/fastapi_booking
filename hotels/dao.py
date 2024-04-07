from datetime import date
from typing import Optional

from sqlalchemy import insert, select, and_

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker,engine
from hotels.models import Hotels
from hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all_date(cls,location):
        async with async_session_maker() as session:
            located = select(Hotels).where(Hotels.location == location)
            booked_room = select(Bookings).where()
            result = await session.execute(located)
            return result.mappings().all()

