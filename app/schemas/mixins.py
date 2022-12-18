# from sqlalchemy.orm import declared_attr
# from sqlalchemy.orm import declarative_mixin
# from sqlalchemy import Column, Integer, Boolean, DateTime
# from sqlalchemy.sql import func
from pydantic import BaseModel, Field, validator, PositiveInt, NonNegativeInt
from datetime import datetime, timedelta

# DATETIME_FORMAT = '%Y-%m-%dT%H:%M'
# FROM_TIME = (datetime.now() + timedelta(minutes=10)).strftime(DATETIME_FORMAT)  #'2023-04-24T11:00'
FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat("T", "minutes")  #'2023-04-24T11:00'
# TO_TIME = (datetime.now() + timedelta(minutes=70)).strftime(DATETIME_FORMAT)
TO_TIME = (datetime.now() + timedelta(minutes=70)).isoformat("T", "minutes")


# @declarative_mixin
class ProjectAndDonationSchemaMixin(BaseModel):
    id: int
    full_amount: PositiveInt
    # invested_amount: PositiveInt = 0
    invested_amount: int
    # fully_invested: bool = Field(False, example=True)
    fully_invested: bool
    # create_date: datetime = Field(datetime.now(), example=FROM_TIME)
    # create_date: datetime = Field(datetime.now())
    create_date: datetime
    # close_date: datetime = Field(None, example=TO_TIME)
    close_date: datetime = None