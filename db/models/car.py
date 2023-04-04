from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from db.db_setup import Base
from db.models.user import User, City


class CarModels(Base):
    """Class for adding the table car_models into the database"""
    __tablename__ = 'car_models'

    id = Column(Integer, primary_key=True)
    model_name = Column(String(60), unique=True, nullable=False)

    def save_to_db(self, db) -> "CarModels":
        db.add(self)
        db.commit()
        return self


class CarCompany(Base):
    """Class for adding the table car_companies into the database"""
    __tablename__ = 'car_companies'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(60), unique=True, nullable=False)

    def save_to_db(self, db) -> "CarCompany":
        db.add(self)
        db.commit()
        return self


class CarCategories(Base):
    """Class for adding the table car_categories into the database"""
    __tablename__ = 'car_categories'

    id = Column(Integer, primary_key=True)
    category = Column(String(60), unique=True, nullable=False)

    def save_to_db(self, db) -> "CarCategories":
        db.add(self)
        db.commit()
        return self


class Car(Base):
    """Class for adding the table cars into the database"""
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    car_id = Column(String(50), unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey('car_companies.id', ondelete='SET NULL'), nullable=True)
    company = relationship("CarCompany", backref=backref("car_companies", uselist=False))
    category_id = Column(Integer, ForeignKey('car_categories.id', ondelete='SET NULL'), nullable=True)
    category = relationship("CarCategories", backref=backref("car_categories", uselist=False))
    model_id = Column(Integer, ForeignKey('car_models.id', ondelete='SET NULL'), nullable=True)
    model = relationship("CarModels", backref=backref("car_models", uselist=False))
    color = Column(String(20), nullable=False)
    mileage = Column(Integer, nullable=False)
    ppd = Column(Integer, nullable=False)
    min_rent = Column(Integer, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='SET NULL'), nullable=True)
    city = relationship(City, backref=backref("cities_cars", uselist=False))
    deposit = Column(Integer, nullable=False)
    status = Column(String(20), nullable=True, default=True)

    def save_to_db(self, db) -> "Car":
        db.add(self)
        db.commit()
        return self


class Rented(Base):
    """Class for adding the table rented into the database"""
    __tablename__ = 'rented'

    booking_id = Column(Integer, primary_key=True)
    carID = Column(Integer, ForeignKey("cars.id", ondelete='SET NULL'), nullable=True)
    car = relationship("Car", backref=backref("cars_rented", uselist=False))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    person = relationship(User, backref=backref("users_rented", uselist=False))
    booking_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    rented_from = Column(DateTime, nullable=False)
    rented_till = Column(DateTime, nullable=False)
    car_taken = Column(Boolean, default=False)
    car_delivery = Column(Boolean, default=False)
    city_taken_id = Column(Integer, ForeignKey('cities.id', ondelete='SET NULL'), nullable=True)
    city_taken = relationship(City, backref=backref("cities_taken", uselist=False), foreign_keys=[city_taken_id])
    city_delivery_id = Column(Integer, ForeignKey('cities.id', ondelete='SET NULL'), nullable=True)
    city_delivery = relationship(City, backref=backref("cities_delivery", uselist=False),
                                 foreign_keys=[city_delivery_id])
    final_status = Column(String(30), default=True)
    said_date = Column(Boolean, default=True)
    said_time = Column(Boolean, default=True)
    proper_condition = Column(Boolean, default=True)
    description = Column(String(200))
    fine = Column(Integer, default=0)
    fine_paid = Column(Boolean, default=False)
