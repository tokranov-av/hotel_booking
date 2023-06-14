import pytest
from httpx import AsyncClient

from app.hotels.router import router

hotels_data = (
    (
        'Алтай', '2023-01-01', '2022-01-10', 400,
        'Дата заезда не может быть позже даты выезда'
    ),
    (
        'Алтай', '2023-01-01', '2023-02-10', 400,
        'Невозможно забронировать отель сроком более месяца'
    ),
    ('Алтай', '2023-01-01', '2023-01-10', 200, None)
)


@pytest.mark.parametrize(
    'location, date_from, date_to, status_code, detail',
    hotels_data
)
async def test_get_hotels_by_location_and_time(
        location,
        date_from,
        date_to,
        status_code,
        detail,
        ac: AsyncClient,
):
    response = await ac.get(
        router.url_path_for(
            'get_hotels_by_location_and_time', location=location
        ),
        params={'date_from': date_from, 'date_to': date_to}
    )
    assert response.status_code == status_code
    if str(status_code).startswith('4'):
        assert response.json()['detail'] == detail
