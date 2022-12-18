# app/schemas/reservation.py
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, root_validator, validator, Extra, Field


DATETIME_FORMAT = '%Y-%m-%dT%H:%M'
# FROM_TIME = (datetime.now() + timedelta(minutes=10)).strftime(DATETIME_FORMAT)  #'2023-04-24T11:00'
FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat("T", "minutes")  #'2023-04-24T11:00'
# TO_TIME = (datetime.now() + timedelta(minutes=70)).strftime(DATETIME_FORMAT)
TO_TIME = (datetime.now() + timedelta(minutes=70)).isoformat("T", "minutes")


class ReservationBase(BaseModel):
    # from_reserve: datetime
    # to_reserve: datetime
    # from_reserve: datetime = Field(..., example='2022-04-24T11:00')
    # to_reserve: datetime = Field(..., example='2022-04-24T12:00')
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):
    
    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values


# Этот класс наследуем от ReservationUpdate с валидаторами.
class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


# Класс ReservationDB нельзя наследовать от ReservationCreate:
# тогда унаследуется и валидатор check_from_reserve_later_than_now,
# и при получении старых объектов из БД он будет выдавать ошибку валидации:
# ведь их from_time вполне может быть меньше текущего времени.

class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    # Добавьте опциональное поле user_id.
    user_id: Optional[int]

    class Config:
        orm_mode = True