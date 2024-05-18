from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from hotels.router import get_hotels

router = APIRouter(
    prefix='/pages',
    tags=['Фронтенд']
)

templates = Jinja2Templates(directory='templates')

@router.get('/hotels')
async def get_hotel_pages(request: Request,hotels=Depends(get_hotels)):
    return templates.TemplateResponse(name='hotels.html',context={'request':request,'hotels':hotels})