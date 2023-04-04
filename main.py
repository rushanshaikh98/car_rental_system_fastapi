from fastapi import FastAPI

from car_rental_system.general.routes import general_router
from db.db_setup import engine
from db.models import user

user.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(general_router)
