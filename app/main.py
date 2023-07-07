# import time
import os
from contextlib import asynccontextmanager
# from urllib.request import Request

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import sentry_sdk
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.importer.router import router as router_import
# from app.logger import logger
from app.pages.router import router as router_pages
from app.prometheus.router import router as router_prometheus
from app.users.router import router_auth, router_users


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

# Подключение эндпоинта для отображения метрик для их дальнейшего
# сбора Prometheus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin.*', '/metrics'],
)

Instrumentator().instrument(app).expose(app)

sentry_sdk.init(
    dsn=('https://98a9ac5895fc4aaeb7d0b0409d2a5c78@o1078497.ingest.sentry.io/'
         '4505398926573568'),
    traces_sample_rate=1.0,
)

app.mount(
    '/static', StaticFiles(directory=os.path.join('app', 'static')), 'static'
)

# Включение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)

# Включение дополнительных роутеров
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_import)
app.include_router(router_prometheus)

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


# @app.middleware('http')
# async def add_process_time_header(request: Request, call_next):
#     """Пример добавления middleware"""
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logger.info(
#         'Время обработки запроса',
#         extra={'process_time': round(process_time, 5)}
#     )
#     response.headers['X-Process-Time'] = str(process_time)
#     return response
