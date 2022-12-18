# app/schemas/meeting_room.py

from typing import Optional

from pydantic import BaseModel, Field, validator


# Базовый класс схемы, от которого наследуем все остальные.
class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


# Теперь наследуем схему не от BaseModel, а от MeetingRoomBase.
class MeetingRoomCreate(MeetingRoomBase):
    # Переопределяем атрибут name, делаем его обязательным.
    name: str = Field(..., min_length=1, max_length=100)
    # Описывать поле description не нужно: оно уже есть в базовом классе.

    @validator('name')
    def name_validator(cls, value: str):
        if not value:
            raise ValueError('Имя обязательно')
        if len(value) > 100:
            raise ValueError('Имя слишком длинное')
        return value


# Новый класс для обновления объектов.
class MeetingRoomUpdate(MeetingRoomBase):
    pass

    @validator('name')
    def name_validator(cls, value: str):
        # if value is None:
        #     raise ValueError('Имя не может быть None/null')
        if not value:
            raise ValueError('Имя обязательно')
        if len(value) > 100:
            raise ValueError('Имя слишком длинное')
        return value


# Возвращаемую схему унаследуем от MeetingRoomCreate, 
# чтобы снова не описывать обязательное поле name.
class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        orm_mode = True