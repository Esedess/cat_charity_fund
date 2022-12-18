from sqlalchemy import Column, Text, Integer, ForeignKey

# from sqlalchemy.orm import relationship

from app.core.db import Base
from .mixins import ProjectAndDonationModelMixin


class Donation(ProjectAndDonationModelMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)