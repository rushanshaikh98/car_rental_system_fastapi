import fastapi
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from car_rental_system.utils.decorators import super_admin_required
from car_rental_system.utils.validators import Validators
from db.db_setup import get_db
from db.models.car import CarCompany, CarCategories, CarModels, Car
from db.models.user import City, User
from car_rental_system.pydantic_schemas.cars import CompanyCreate, CategoryCreate, ModelCreate, CompanyAll, CategoryAll, ModelAll, \
    CompanyDelete, CategoryDelete, ModelDelete
from car_rental_system.pydantic_schemas.users import CityCreate, UserCreate, CityAll, CityDelete

router = fastapi.APIRouter()


@router.post('/create_admin', status_code=201)
@super_admin_required()
async def create_admin(admin: UserCreate, db: Session = Depends(get_db)):
    try:
        error = Validators.validate_email(admin.email, db)
        if error:
            raise HTTPException(status_code=400, detail=error)
        error = Validators.validate_username(admin.username, db)
        if error:
            raise HTTPException(status_code=400, detail=error)
        error = Validators.validate_password(admin.password)
        if error:
            raise HTTPException(status_code=400, detail=error)
        city = db.query(City).filter_by(city=admin.city.replace(" ", "").upper()).first()
        if not city:
            raise HTTPException(status_code=400, detail="City not Found!")
        hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(admin.password)
        admin_object = User(name=admin.name, username=admin.username, email=admin.email,
                            password=hashed_password, city_id=city.id, is_admin=True)
        admin_object.save_to_db(db)
        return {"data": admin,
                "message": "User Registered Successfully!"}
    except (KeyError, AttributeError) as error:
        print(admin)
        raise HTTPException(status_code=400, detail=error)


@router.post('/add_city', status_code=201)
async def add_city(city_data: CityCreate, db: Session = Depends(get_db)):
    try:
        city = db.query(City).filter_by(city=city_data.city.replace(" ", "").upper()).first()
        if city:
            raise HTTPException(status_code=400, detail="City already exists!")
        city_object = City(city=city_data.city.replace(" ", "").upper())
        city_object.save_to_db(db)
        return {"data": city_data,
                "message": "City Added Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.post('/add_company', status_code=201)
async def add_company(company_data: CompanyCreate, db: Session = Depends(get_db)):
    try:
        company = db.query(CarCompany).filter_by(
            company_name=company_data.company_name.replace(" ", "").upper()).first()
        if company:
            raise HTTPException(status_code=400, detail="Company already exists!")
        company_object = CarCompany(company_name=company_data.company_name.replace(" ", "").upper())
        company_object.save_to_db(db)
        return {"data": company_data,
                "message": "Company Added Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.post('/add_category', status_code=201)
async def add_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        category = db.query(CarCategories).filter_by(category=category_data.category.replace(" ", "").upper()).first()
        if category:
            raise HTTPException(status_code=400, detail="Category already exists!")
        category_object = CarCategories(category=category_data.category.replace(" ", "").upper())
        category_object.save_to_db(db)
        return {"data": category_data,
                "message": "Category Added Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.post('/add_model', status_code=201)
async def add_model(model_data: ModelCreate, db: Session = Depends(get_db)):
    try:
        model = db.query(CarModels).filter_by(model_name=model_data.model_name.replace(" ", "").upper()).first()
        if model:
            raise HTTPException(status_code=400, detail="Model already exists!")
        model_object = CarModels(model_name=model_data.model_name.replace(" ", "").upper())
        model_object.save_to_db(db)
        return {"data": model_data,
                "message": "Model Added Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.patch('/update_city', status_code=200)
async def update_city(city_data: CityAll, db: Session = Depends(get_db)):
    try:
        city_id = db.query(City).filter_by(id=city_data.id).first()
        if not city_id:
            raise HTTPException(status_code=404, detail="City id does not exist!")
        city = db.query(City).filter_by(city=city_data.city.replace(" ", "").upper()).first()
        if city:
            raise HTTPException(status_code=400, detail="City already exists!")
        city_id.city = city_data.city.replace(" ", "").upper()
        db.commit()
        return {"data": city_data,
                "message": "City updated Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.patch('/update_company', status_code=200)
async def update_company(company_data: CompanyAll, db: Session = Depends(get_db)):
    try:
        company_id = db.query(CarCompany).filter_by(id=company_data.id).first()
        if not company_id:
            raise HTTPException(status_code=404, detail="Company id does not exist!")
        company = db.query(CarCompany).filter_by(
            company_name=company_data.company_name.replace(" ", "").upper()).first()
        if company:
            raise HTTPException(status_code=400, detail="Company already exists!")
        company_id.company_name = company_data.company_name.replace(" ", "").upper()
        db.commit()
        return {"data": company_data,
                "message": "Company updated Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.patch('/update_category', status_code=200)
async def update_category(category_data: CategoryAll, db: Session = Depends(get_db)):
    try:
        category_id = db.query(CarCategories).filter_by(id=category_data.id).first()
        if not category_id:
            raise HTTPException(status_code=404, detail="Category id does not exist!")
        category = db.query(CarCategories).filter_by(category=category_data.category.replace(" ", "").upper()).first()
        if category:
            raise HTTPException(status_code=400, detail="Category already exists!")
        category_id.category = category_data.category.replace(" ", "").upper()
        db.commit()
        return {"data": category_data,
                "message": "Category updated Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.patch('/update_model', status_code=200)
async def update_model(model_data: ModelAll, db: Session = Depends(get_db)):
    try:
        model_id = db.query(CarModels).filter_by(id=model_data.id).first()
        if not model_id:
            raise HTTPException(status_code=404, detail="model id does not exist!")
        model = db.query(CarModels).filter_by(model_name=model_data.model_name.replace(" ", "").upper()).first()
        if model:
            raise HTTPException(status_code=400, detail="Model already exists!")
        model_id.model_name = model_data.model_name.replace(" ", "").upper()
        db.commit()
        return {"data": model_data,
                "message": "Model updated Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.delete('/delete_city', status_code=200)
async def delete_city(city_data: CityDelete, db: Session = Depends(get_db)):
    try:
        city_id = db.query(City).filter_by(id=city_data.id).first()
        if not city_id:
            raise HTTPException(status_code=404, detail="City id does not exist!")
        users = db.query(User).filter_by(city_id=city_data.id).first()
        if users:
            raise HTTPException(status_code=400, detail="City cannot be deleted as it has users!")
        db.delete(city_id)
        db.commit()
        return {"message": "City deleted Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.delete('/delete_company', status_code=200)
async def delete_company(company_data: CompanyDelete, db: Session = Depends(get_db)):
    try:
        company_id = db.query(CarCompany).filter_by(id=company_data.id).first()
        if not company_id:
            raise HTTPException(status_code=404, detail="Company id does not exist!")
        cars = db.query(Car).filter_by(company_id=company_data.id).first()
        if cars:
            raise HTTPException(status_code=400,
                                detail="Company cannot be deleted as our company owns some cars of this company!")
        db.delete(company_id)
        db.commit()
        return {"message": "Company deleted Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.delete('/delete_category', status_code=200)
async def delete_category(category_data: CategoryDelete, db: Session = Depends(get_db)):
    try:
        category_id = db.query(CarCategories).filter_by(id=category_data.id).first()
        if not category_id:
            raise HTTPException(status_code=404, detail="Category id does not exist!")
        cars = db.query(Car).filter_by(category_id=category_data.id).first()
        if cars:
            raise HTTPException(status_code=400,
                                detail="Category cannot be deleted as our company owns some cars of this category!")
        db.delete(category_id)
        db.commit()
        return {"message": "Category deleted Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)


@router.delete('/delete_model', status_code=200)
async def delete_model(model_data: ModelDelete, db: Session = Depends(get_db)):
    try:
        model_id = db.query(CarModels).filter_by(id=model_data.id).first()
        if not model_id:
            raise HTTPException(status_code=404, detail="Model id does not exist!")
        cars = db.query(Car).filter_by(model_id=model_data.id).first()
        if cars:
            raise HTTPException(status_code=400,
                                detail="Model cannot be deleted as our company owns some cars of this model!")
        db.delete(model_id)
        db.commit()
        return {"message": "Model deleted Successfully!"}

    except (KeyError, AttributeError) as error:
        raise HTTPException(status_code=400, detail=error)
