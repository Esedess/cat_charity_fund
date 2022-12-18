from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator, PositiveInt
from .mixins import ProjectAndDonationSchemaMixin


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    # @validator('full_amount')
    # def full_amount_validator(cls, value: PositiveInt):
    #     if not value:
    #         raise ValueError('Требуемая сумма обязательна!')
    #     # if len(value) < 0:
    #     #     raise ValueError('Не может быть меньше нуля.')
    #     return value


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('full_amount')
    def full_amount_validator(cls, value: PositiveInt):
        if not value:
            raise ValueError('Требуемая сумма обязательна!')
        # if len(value) < 0:
        #     raise ValueError('Не может быть меньше нуля.')
        return value


# class CharityProjectDB(ProjectAndDonationSchemaMixin, CharityProjectCreate):
class CharityProjectDB(CharityProjectCreate):
    id: int
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
    # close_date: datetime = None

    class Config:
        orm_mode = True