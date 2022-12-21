from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixins import ProjectAndDonationModelMixin


class Donation(ProjectAndDonationModelMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
