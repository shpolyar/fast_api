from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str
    price: int


class ProductResponse(ProductCreate):
    id: int


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(UserCreate):
    id: int

