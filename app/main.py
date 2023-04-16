from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            stars: Optional[int] = Query(default=None, ge=1, le=5),
            has_spa: Optional[bool] = None
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


# @app.get('/hotels', response_model=list[SHotel])
# def get_hotels(
#         location: str,
#         date_from: date,
#         date_to: date,
#         stars: Optional[int] = Query(default=None, ge=1, le=5),
#         has_spa: Optional[bool] = None
# ):
#     data = {
#         'location': location,
#         'date_from': date_from,
#         'date_to': date_to,
#         'stars': stars,
#         'has_spa': has_spa
#     }
#     print(data)
#     hotels = [
#         {
#             'address': 'ул. Гагарина, д.1, Алтай', 'name': 'Super Hotel',
#             'stars': 5
#         },
#     ]
#     return hotels

@app.get('/hotels', response_model=list[SHotel])
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
):
    print(search_args)
    hotels = [
        {
            'address': 'ул. Гагарина, д.1, Алтай', 'name': 'Super Hotel',
            'stars': 5
        },
    ]
    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SBooking):
    pass















