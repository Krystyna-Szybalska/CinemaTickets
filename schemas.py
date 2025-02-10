# Pydantic models (data validation for API requests)
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True  # Tells Pydantic to work with SQLAlchemy models


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    phone_number: str
    name: str


class ShowingResponse(BaseModel):
    movie_title: str
    showing_date: datetime
    hall_id: int
    hall_name: str


class SeatResponse(BaseModel):
    seat_id: str
    seat_number: int
    row_number: int


class ShowingDetailResponse(BaseModel):
    showing_id: str
    movie: str
    hall_name: str
    available_seats: list[SeatResponse]


class ReservationRequest(BaseModel):
    showing_id: str
    user_id: str
    seat_ids: list[str]  # List of seat IDs
