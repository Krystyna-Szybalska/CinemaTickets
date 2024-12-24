# Pydantic models (data validation)
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True  # Tells Pydantic to work with SQLAlchemy models
