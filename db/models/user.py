import os

from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from db.db_setup import Base


class City(Base):
    """Class for adding the table cities into the database"""
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city = Column(String(60), unique=True, nullable=False)

    def save_to_db(self, db) -> "City":
        db.add(self)
        db.commit()
        return self


class User(Base):
    """Class for adding the table users into the database"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='SET NULL'), nullable=True)
    city = relationship("City", backref=backref("cities_users", uselist=False))
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)
    fine_pending = Column(Boolean, default=False)

    def save_to_db(self, db) -> "User":
        db.add(self)
        db.commit()
        return self

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(os.environ.get("SECRET_KEY"), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.environ.get("SECRET_KEY"))
        try:
            user_id = s.loads(token)['user_id']
        except ValueError:
            return None
        return User.query.get(user_id)
