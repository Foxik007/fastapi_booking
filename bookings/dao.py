from fastapi import HTTPException
from sqlalchemy.orm import aliased

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker, engine
from exception import NotBookings
from hotels.rooms.models import Rooms

from datetime import date

from sqlalchemy import and_, func, insert, select, delete


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_by_user(cls,user_id):
        async with async_session_maker() as session:
            r = aliased(Rooms)
            b = aliased(Bookings)

            query = (select(
                b.id,
                b.room_id,
                b.user_id,
                b.date_from,
                b.date_to,
                b.price,
                b.total_cost,
                b.total_days,
                r.image_id,
                r.name,
                r.description,
                r.services,
            ).filter(b.user_id == user_id)
                     .select_from(b)
                     .join(r, b.room_id == r.id, isouter=True)
            )
            result = await session.execute(query)
            return result.mappings().all()



    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                #ИЩЕМ ВСЕ ПЕРЕСЕКАЮЩИЕСЯ ДАТЫ В БАЗЕ ДАННЫХ И ВЫВОДИМ ИХ
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            and_(
                                Bookings.date_from < date_to,
                                Bookings.date_to > date_from,
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                print(booked_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
                """
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
                """

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id).filter(
                            booked_rooms.c.room_id.is_not(None))).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # Рекомендую выводить SQL запрос в консоль для сверки
                # logger.debug(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(
                            Bookings.id,
                            Bookings.user_id,
                            Bookings.room_id,
                            Bookings.date_from,
                            Bookings.date_to,
                        )
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.mappings().one()
                else:
                    raise HTTPException(status_code=401)
        except HTTPException:
            raise HTTPException(status_code=401)

    @classmethod
    async def delete(cls,**filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            result: int = result.scalar()
            if result == None:
                raise NotBookings
            else:
                query = delete(cls.model).filter_by(**filter_by)
                await session.execute(query)
                await session.commit()

