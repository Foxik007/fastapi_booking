import time
from contextlib import asynccontextmanager
from urllib.request import Request
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi_versioning import VersionedFastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from admin.auth import authentication_backend
from admin.views import BookingsAdmin, HotelAdmin, RoomAdmin, UserAdmin
from bookings.router import router as router_bookings
from config import settings
from database import engine
from hotels.rooms.router import router as router_rooms
from hotels.router import router as router_hotel
from images.router import router as router_images
from logger import logger
from pages.router import router as router_pages
from users.router import router as router_user
from fastapi import FastAPI
import sentry_sdk

@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении
    print("Выключен")


app = FastAPI(lifespan=lifespan)


sentry_sdk.init(
    dsn="https://08eb5ad6bbe931e479b234cbd6ab2be8@o4507350397419520.ingest.de.sentry.io/4507350401548368",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_hotel)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # logger.info('request handling time',extra={
    #     'process_time': round(process_time,4)
    # })
    return response


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)
app.mount("/static", StaticFiles(directory="static"), "static")
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)
