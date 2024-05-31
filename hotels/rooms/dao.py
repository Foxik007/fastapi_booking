from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import aliased

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker
from hotels.models import Hotels
from hotels.rooms.models import Rooms
from hotels.rooms.schemas import sAvailableRoom


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_by_hotel(cls,
                                 hotel_id:int,
                                 date_from:date,
                                 date_to:date,
                                 ) -> list[sAvailableRoom]:
        async with async_session_maker() as session:
            r = aliased(Rooms)
            b = aliased(Bookings)
            h = aliased(Hotels)
            #Найдем занятые комнаты на даты
            relbook = (select(
                r.id,
                func.count().label('booked_rooms'))
                .select_from(r)
                .join(b,r.id == b.room_id)
                .filter(b.date_from <= date_to,
                        b.date_to >= date_from)
            ).group_by(r.id).cte('rb')
            relhot = (select(h)
                      .select_from(h)
                      .filter(h.id == hotel_id)
                      ).cte('rh')
            # print('RB SQL')
            # print(relbook.compile(compile_kwargs={'literal_binds':True}))

            query = (select(
                relhot.c.id.label('hotel_id'),
                r.id,
                r.name,
                r.description,
                r.services,
                r.price,
                r.quantity,
                r.image_id,
                ((date_to - date_from).days * r.price).label('total_cost'),
                (r.quantity - func.coalesce(relbook.c.booked_rooms,0)).label('rooms_left'))
                .select_from(relhot)
                .join(r, relhot.c.id == r.hotel_id)
                .join(relbook,r.id == relbook.c.id,isouter=True)
                    )

            res = await session.execute(query)
            return res.mappings().all()
