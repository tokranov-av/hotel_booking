from datetime import datetime

import pytest

from app.bookings.dao import BookingDAO


@pytest.mark.parametrize(
    'user_id, room_id',
    [(2, 2), (2, 3), (1, 4), (1, 4)]
)
async def test_booking_crud(user_id, room_id):
    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime('2023-07-10', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-07-24', '%Y-%m-%d')
    )
    print(new_booking)
    assert new_booking.get('user_id') == user_id
    assert new_booking.get('room_id') == room_id

    # new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
