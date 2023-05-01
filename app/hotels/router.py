import asyncio
from datetime import date, datetime, timedelta
from pprint import pprint
from typing import List, Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as

from app.exceptions import (
    CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
)
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo


router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('/{location}')
@cache(expire=60)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(
        ...,
        description=f'Например, {datetime.now().date()}'
    ),
    date_to: date = Query(
        ...,
        description=f'Например, {(datetime.now() + timedelta(days=14)).date()}'
    ),
):
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    await asyncio.sleep(3)
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    # Здесь используется parse_obj_as исключительно потому,
    # что это нужно для кэширования библиотекой fastapi-cache.
    # Обычно мы прописываем response_model для валидации и сериализации данных
    hotels_parse = parse_obj_as(List[SHotelInfo], hotels)
    return hotels_parse


@router.get("/id/{hotel_id}", include_in_schema=True)
# Этот эндпоинт используется для фронтенда, когда мы хотим отобразить все
# номера в отеле и информацию о самом отеле. Этот эндпоинт как раз отвечает за
# информацию об отеле.
# В нем нарушается правило именования эндпоинтов: конечно же, /id/ здесь
# избыточен.
# Тем не менее он используется, так как эндпоинтом ранее мы уже задали
# получение отелей по их локации вместо id.
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelDAO.find_one_or_none(id=hotel_id)

