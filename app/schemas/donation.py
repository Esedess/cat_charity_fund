from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator, PositiveInt, Extra
from .mixins import ProjectAndDonationSchemaMixin


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    ...

    # class Config:
    #     extra = Extra.forbid
        # fields = {'user_id': {'exclude': True}}
        # __exclude_fields__ = 'user_id'

    # @validator('full_amount')
    # def full_amount_validator(cls, value: PositiveInt):
    #     if not value:
    #         raise ValueError('Требуемая сумма обязательна!')
    #     # if len(value) < 0:
    #     #     raise ValueError('Не может быть меньше нуля.')
    #     return value


# class DonationUpdate(DonationBase):
#     pass

    # @validator('full_amount')
    # def full_amount_validator(cls, value: PositiveInt):
    #     if not value:
    #         raise ValueError('Требуемая сумма обязательна!')
    #     # if len(value) < 0:
    #     #     raise ValueError('Не может быть меньше нуля.')
    #     return value


class DonationMiniDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationMiniDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime

    class Config:
        orm_mode = True