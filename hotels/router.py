import asyncio
from datetime import date
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from hotels.dao import HotelDAO

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/location')
# @cache(expire=20)
async def get_hotels(location: str, date_from: date, date_to: date):
    # await asyncio.sleep(3)
    return await HotelDAO.find_available_hotels(location, date_from, date_to)


@router.post('/add')
async def add_hotels(name: str, rooms_quantity: int, image_id: int, location: str, services: str):
    await HotelDAO.add(name=name, location=location,
                       services=services, rooms_quantity=rooms_quantity, image_id=image_id)
    return f'Отель {name} добавлен'


@router.delete('/delete')
async def delete_hotel(name):
    await HotelDAO.delete(name=name)
    return 'Успешно удален(а)'
