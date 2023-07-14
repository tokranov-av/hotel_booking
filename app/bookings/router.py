from fastapi import APIRouter, Depends  # BackgroundTasks
from pydantic.type_adapter import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get('')
async def get_bookings(
        user: Users = Depends(get_current_user)
) -> list[SBookingInfo]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post('', status_code=201)
async def add_booking(
    booking: SNewBooking,
    # background_tasks: BackgroundTasks,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=booking.room_id,
        date_from=booking.date_from,
        date_to=booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    # Celery
    send_booking_confirmation_email.delay(booking, user.email)
    # Background Tasks
    # background_tasks.add_task(
    # send_booking_confirmation_email, booking, user.email)
    return booking


@router.delete('/{booking_id}', status_code=204)
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
