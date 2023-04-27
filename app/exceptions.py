from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже существует',
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный email или пароль',
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истёк',
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен отсутствует',
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный формат токена',
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)

RoomCannotBeBookedException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не осталось свободных номеров',
)

DateFromCannotBeAfterDateTo = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Дата заезда не может быть позже даты выезда",
)

CannotBookHotelForLongPeriod = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Невозможно забронировать отель сроком более месяца",
)

CannotAddDataToDatabase = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Не удалось добавить запись",
)
