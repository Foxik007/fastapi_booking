from typing import Optional

from fastapi import APIRouter

from hotels.dao import HotelDAO
from hotels.schemas import SHotels

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)
@router.get('')
async def get_hotels():
    return await HotelDAO.find_all()


@router.post('/hotels')
async def add_hotels(name:str,rooms_quantity:int,image_id:int,location:str,services:str):
    await HotelDAO.add(name=name,location=location,
                       services=services,rooms_quantity=rooms_quantity,image_id=image_id)
    return f'Отель {name} добавлен'


@router.delete('')
async def delete_hotel(name):
    await HotelDAO.delete(name=name)
    return 'Успешно удален(а)'


@router.get('/location')
async def get_hotels_location(location):
    return await HotelDAO.find_all_date(location=location)