from pydantic import BaseModel


class CompanyBase(BaseModel):
    company_name: str


class CompanyDelete(BaseModel):
    id: int


class CompanyCreate(CompanyBase):
    ...


class CompanyAll(CompanyDelete, CompanyBase):
    ...

    class Config:
        orm_mode = True


class ModelBase(BaseModel):
    model_name: str


class ModelDelete(BaseModel):
    id: int


class ModelCreate(ModelBase):
    ...


class ModelAll(ModelDelete, ModelBase):
    ...

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    category: str


class CategoryDelete(BaseModel):
    id: int


class CategoryCreate(CategoryBase):
    ...


class CategoryAll(CategoryDelete, CategoryBase):
    ...

    class Config:
        orm_mode = True
