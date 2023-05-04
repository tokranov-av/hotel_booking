from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password, ]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class HotelsAdmin(ModelView, model=Hotels):
    column_list = Hotels.__table__.columns.keys()
    column_list.append(Hotels.rooms)
    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'


class RoomsAdmin(ModelView, model=Rooms):
    column_list = Rooms.__table__.columns.keys()
    column_list.extend([Rooms.hotel, Rooms.booking])
    name = 'Номер'
    name_plural = 'Номера'
    icon = 'fa-solid fa-bed'


class BookingsAdmin(ModelView, model=Bookings):
    column_list = Bookings.__table__.columns.keys()
    column_list.extend([Bookings.user, Bookings.room])
    name = 'Бронь'
    name_plural = 'Брони'
    icon = 'fa-solid fa-book'
