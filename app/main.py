from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.admin.auth import authentication_backend
from app.admin.views import UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.users.router import router_auth, router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from app.importer.router import router as router_import


# Подключение к redis перед запуском приложения
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
        encoding='utf8',
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    yield

# @app.on_event('startup')
# async def startup():
#     redis = aioredis.from_url(
#         'redis://localhost:6379', encoding='utf8', decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix='cache')


app = FastAPI(
    title='Бронирование отелей',
    lifespan=lifespan
)
app.mount('/static', StaticFiles(directory='app/static'), 'static')

# Включение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)

# Включение дополнительных роутеров
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_import)

# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin', 'Authorization'
    ],
)


# Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)
