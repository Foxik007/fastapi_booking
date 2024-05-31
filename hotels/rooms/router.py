from datetime import date

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bookings.models import Bookings
from database import async_session_maker
from hotels.models import Hotels
from hotels.rooms.dao import RoomsDAO
from hotels.rooms.models import Rooms

router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel(hotel_id: int, date_from: date, date_to: date):
    return await RoomsDAO.get_rooms_by_hotel(hotel_id, date_from, date_to)


@router.get('/example/no_orm')
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms.__table__.columns, Hotels.__table__.columns, Bookings.__table__.columns)
            .join(Hotels, Rooms.hotel_id == Hotels.id)
            .join(Bookings,Bookings.room_id == Rooms.id)
        )
        res = await session.execute(query)
        res = res.mappings().all()
        return res


@router.get('/example/orm')
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms)
            .options(selectinload(Rooms.hotel))
            .options(selectinload(Rooms.bookings))
        )
        res = await session.execute(query)
        res = res.scalars().all()
        res = jsonable_encoder(res)
        return res