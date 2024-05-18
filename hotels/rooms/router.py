from datetime import date
from fastapi import APIRouter
from hotels.rooms.dao import RoomsDAO

router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel(hotel_id: int, date_from: date, date_to: date):
    return await RoomsDAO.get_rooms_by_hotel(hotel_id, date_from, date_to)
