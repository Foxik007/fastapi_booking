from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 401  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class TokenExpired(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек'

class NotBookings(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Такой брони мы не нашли'

