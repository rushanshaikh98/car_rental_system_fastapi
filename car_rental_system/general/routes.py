import fastapi
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from car_rental_system.general.services import UserServices
from car_rental_system.pydantic_schemas.users import UserCreate, Token, UserLogin
from car_rental_system.utils.other_utils import get_current_user
from db.db_setup import get_db

general_router = fastapi.APIRouter()


def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserServices.register(user, db)


def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return UserServices.login(user_data, db)


def read_users_me(token: Token, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    return get_current_user(db, token)


general_router.add_api_route("/register", register_user, methods=["POST"], status_code=status.HTTP_201_CREATED)
general_router.add_api_route("/login", login_user, methods=["POST"], status_code=status.HTTP_200_OK)
general_router.add_api_route("", login_user, methods=["POST"], status_code=status.HTTP_200_OK)
