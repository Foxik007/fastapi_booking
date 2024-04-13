from datetime import date
from typing import Optional
from fastapi import APIRouter
from hotels.dao import HotelDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)
@router.get('/location')
async def get_hotels(location:str,date_from:date,date_to:date):
    return await HotelDAO.find_available_hotels(location,date_from,date_to)


@router.post('/add')
async def add_hotels(name:str,rooms_quantity:int,image_id:int,location:str,services:str):
    await HotelDAO.add(name=name,location=location,
                       services=services,rooms_quantity=rooms_quantity,image_id=image_id)
    return f'Отель {name} добавлен'


@router.delete('/delete')
async def delete_hotel(name):
    await HotelDAO.delete(name=name)
    return 'Успешно удален(а)'

