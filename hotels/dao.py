from datetime import date

from sqlalchemy import insert, select, and_, func
from sqlalchemy.orm import aliased

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker
from hotels.models import Hotels
from hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_available_hotels(cls,location:str,date_from:date,date_to:date):
        async with (async_session_maker() as session):
            r = aliased(Rooms)
            b = aliased(Bookings)
            h = aliased(Hotels)

            bfd = (select(b).filter
                   (and_(
                        b.date_from <= date_to,
                        b.date_to >= date_from)
            )).cte('bfd)')

            rb = (select(r.hotel_id,func.count().label('booked_rooms'))
                  .select_from(r)
                  .join(bfd,r.id == bfd.c.room_id)
                  .group_by(r.hotel_id).cte('rb'))

            query = (select(
                h.id,
                h.name,
                h.location,
                h.services,
                h.rooms_quantity,
                h.image_id,
                (h.rooms_quantity - func.coalesce(rb.c.booked_rooms,0)).label('rooms_left'))
                .select_from(h)
                .join(rb, h.id == rb.c.hotel_id,isouter=True)
                .filter(
                    h.location.contains(location),
                    (h.rooms_quantity - func.coalesce(rb.c.booked_rooms,0)) > 0

            ))
            res = await session.execute(query)
            return res.mappings().all()
