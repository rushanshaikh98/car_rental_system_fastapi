from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase, UserLogin):
    name: str
    city: str


class UserAll(UserBase):
    id: int
    is_verified: bool
    is_admin: bool
    is_super_admin: bool
    fine_pending: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserInDB(UserAll):
    hashed_password: str


class CityBase(BaseModel):
    city: str


class CityDelete(BaseModel):
    id: int


class CityCreate(CityBase):
    ...


class CityAll(CityDelete, CityBase):
    ...

    class Config:
        orm_mode = True
