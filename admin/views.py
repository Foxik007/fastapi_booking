from sqladmin import ModelView

from bookings.models import Bookings
from hotels.models import Hotels
from hotels.rooms.models import Rooms
from users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id,Users.email,Users.bookings]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    column_details_exclude_list = [Users.hashed_password]
    name = 'Пользователь'
    name_plural = 'Пользователи'

class BookingsAdmin(ModelView, model=Bookings):
    column_list = '__all__'
    can_create = True
    can_edit = True
    can_view_details = True
    name = 'Бронь'
    name_plural = 'Брони'

    def __str__(self):
        return f'{self.id}'

class RoomAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    can_create = True
    can_edit = True
    can_view_details = True
    name = 'Номер'
    name_plural = 'Номера'

    def __str__(self):
        return f'{self.id}'

class HotelAdmin(ModelView, model=Hotels):
    column_list = [i.name for i in Hotels.__table__.c] + [Hotels.rooms]
    can_create = True
    can_edit = True
    can_view_details = True
    name = 'Отели'
    name_plural = 'Отели'


    def __str__(self):
        return f'{self.id}'

