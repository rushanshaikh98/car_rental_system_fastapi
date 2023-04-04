from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from db.db_setup import Base
from db.models.user import City, User


class Temporary(Base):
    """Class for adding the table temporary into the database"""
    __tablename__ = 'temporary'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    person = relationship(User, backref=backref("users_temp", uselist=False))
    booking_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    rent_from = Column(DateTime, nullable=False)
    rent_till = Column(DateTime, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='SET NULL'), nullable=True)
    city = relationship(City, backref=backref("cities_temp", uselist=False))
