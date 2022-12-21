from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, NonNegativeInt, PositiveInt,
                      validator)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    ...

    @validator('full_amount')
    def full_amount_validator(cls, value: PositiveInt):
        if not value:
            raise ValueError('Требуемая сумма обязательна!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    full_amount: PositiveInt
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
