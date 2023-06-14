import pytest

from app.hotels.dao import HotelDAO

hotels_data = (
    (1, True),
    (6, True),
    (7, False)
)


@pytest.mark.parametrize('hotel_id, is_present', hotels_data)
async def test_find_hotel_by_id(hotel_id, is_present):
    hotel = await HotelDAO.find_one_or_none(id=hotel_id)

    if is_present:
        assert hotel
        assert hotel['id'] == hotel_id
    else:
        assert not hotel
