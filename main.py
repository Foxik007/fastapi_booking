from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from admin.views import UserAdmin, BookingsAdmin, RoomAdmin, HotelAdmin
from bookings.router import router as router_bookings
from config import settings
from database import engine
from users.models import Users
from users.router import router as router_user
from hotels.router import router as router_hotel
from hotels.rooms.router import router as router_rooms
from pages.router import router as router_pages
from images.router import router as router_images
from fastapi_cache import FastAPICache
from contextlib import asynccontextmanager
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import FastAPI
from sqladmin import Admin, ModelView

@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении
    print('Выключен')

app = FastAPI(lifespan=lifespan)


admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)

app.mount('/static', StaticFiles(directory='static'),'static')

app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_hotel)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)



