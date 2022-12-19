# from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import declarative_mixin
from sqlalchemy import Column, Integer, Boolean, DateTime, DATETIME
from sqlalchemy.sql import func
from datetime import datetime


@declarative_mixin
class ProjectAndDonationModelMixin:
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    def not_invested(self) -> int:
        return self.full_amount - self.invested_amount

    def invest(self, investition=0):
        if investition > self.not_invested():
            return
        self.invested_amount += investition
        if self.full_amount == self.invested_amount:
            self.fully_invested = True
            # self.close_date = func.now()
            self.close_date = datetime.now()