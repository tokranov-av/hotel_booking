from datetime import date

from sqlalchemy import select, and_, or_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import engine, async_session_maker
from app.hotels.models import Rooms


class BookingDAO(BaseDAO):
    """
    with booked_rooms as (
    select * from bookings where room_id = 1 and
     ('2023-05-15' <= date_from and date_from <= '2023-06-20') or
      (date_from <= '2023-05-15' and '2023-05-15' <= date_to)
    )

    select rooms.quantity - count(booked_rooms.room_id) from rooms
     left join booked_rooms on booked_rooms.room_id = rooms.id
      where rooms.id = 1
       group by rooms.quantity, booked_rooms.room_id;
    """
    model = Bookings

    @classmethod
    async def add(
            cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            date_from <= Bookings.date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            date_from <= Bookings.date_to
                        )
                    )
                )
            ).cte('booked_rooms')

            rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            print(rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            rooms_left = await session.execute(rooms_left)
            print(rooms_left.scalar())
