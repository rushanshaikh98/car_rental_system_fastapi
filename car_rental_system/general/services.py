from datetime import timedelta

import fastapi
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from car_rental_system.pydantic_schemas.users import Token, UserLogin
from car_rental_system.utils.other_utils import authenticate_user, create_access_token, get_current_user
from car_rental_system.utils.validators import Validators
from db.db_setup import get_db
from db.models.user import City, User

router = fastapi.APIRouter()


class UserServices:
    @staticmethod
    def register(user, db):
        try:
            error = Validators.validate_email(user.email, db)
            if error:
                raise HTTPException(status_code=400, detail=error)
            error = Validators.validate_username(user.username, db)
            if error:
                raise HTTPException(status_code=400, detail=error)
            error = Validators.validate_password(user.password)
            if error:
                raise HTTPException(status_code=400, detail=error)
            city = db.query(City).filter_by(city=user.city.replace(" ", "").upper()).first()
            if not city:
                raise HTTPException(status_code=400, detail="City not Found!")
            hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)
            user_object = User(name=user.name, username=user.username, email=user.email, password=hashed_password,
                               city_id=city.id)
            user_object.save_to_db(db)
            return {"data": user, "message": "User Registered Successfully!"}
        except (KeyError, AttributeError) as error:
            raise HTTPException(status_code=400, detail=error)

    @staticmethod
    def login(user_data, db):
        user = authenticate_user(db, user_data.username, user_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}


