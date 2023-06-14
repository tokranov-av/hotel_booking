import pytest
from httpx import AsyncClient

from app.bookings.router import router


booking_data = (
    (4, '2030-05-01', '2030-05-15', 3, 201),
    (4, '2030-05-02', '2030-05-16', 4, 201),
    (4, '2030-05-03', '2030-05-17', 5, 201),
    (4, '2030-05-04', '2030-05-18', 6, 201),
    (4, '2030-05-05', '2030-05-19', 7, 201),
    (4, '2030-05-06', '2030-05-20', 8, 201),
    (4, '2030-05-07', '2030-05-21', 9, 201),
    (4, '2030-05-08', '2030-05-22', 10, 201),
    (4, '2030-05-09', '2030-05-23', 10, 409),
    (4, '2030-05-10', '2030-05-24', 10, 409)
)


@pytest.mark.parametrize(
    'room_id, date_from, date_to, booked_rooms, status_code',
    booking_data
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        router.url_path_for('get_bookings'),
        json={'room_id': room_id, 'date_from': date_from, 'date_to': date_to}
    )

    assert response.status_code == status_code

    response = await authenticated_ac.get(router.url_path_for('get_bookings'))
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get(router.url_path_for('get_bookings'))
    existing_bookings = [booking['id'] for booking in response.json()]
    for booking_id in existing_bookings:
        response = await authenticated_ac.delete(
            router.url_path_for('remove_booking', booking_id=booking_id),
        )
        assert response.status_code == 204
    response = await authenticated_ac.get(router.url_path_for('get_bookings'))
    assert len(response.json()) == 0
