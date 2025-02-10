# SQLAlchemy models and database setup
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


# User table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Store UUID as string
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(15))
    password = Column(String(100), nullable=False)
    is_guest = Column(Boolean, default=False)  # New column added


# Movies table
class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    genre = Column(String(50))
    duration_minutes = Column(Integer)
    rating = Column(String(10))
    ticket_price = Column(Float, nullable=False)
    release_date = Column(Date)


# Halls table
class Hall(Base):
    __tablename__ = 'halls'
    hall_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    seats = relationship('Seat', back_populates='hall')


# Seats table
class Seat(Base):
    __tablename__ = 'seats'
    seat_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hall_id = Column(String(36), ForeignKey('halls.hall_id'), nullable=False)
    seat_number = Column(Integer, nullable=False)
    row_number = Column(Integer, nullable=False)
    hall = relationship('Hall', back_populates='seats')
    reserved_seats = relationship('ReservedSeat', back_populates='seat')  # Add this


# Showings table
class Showing(Base):
    __tablename__ = 'showings'
    showing_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    hall_id = Column(Integer, ForeignKey('halls.hall_id'), nullable=False)
    showing_date = Column(DateTime, nullable=False)
    movie = relationship('Movie')
    hall = relationship('Hall')


# Reservations table
class Reservation(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    showing_id = Column(String(36), ForeignKey('showings.showing_id'), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    user = relationship('User')
    showing = relationship('Showing')
    reserved_seats = relationship('ReservedSeat', back_populates='reservation')  # Add this


# Reserved_Seats table
class ReservedSeat(Base):
    __tablename__ = 'reserved_seats'
    reserved_seat_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reservation_id = Column(String(36), ForeignKey('reservations.reservation_id'), nullable=False)
    seat_id = Column(String(36), ForeignKey('seats.seat_id'), nullable=False)
    ticket_type = Column(String(20), nullable=False)
    ticket_price = Column(Float, nullable=False)
    reservation = relationship('Reservation', back_populates='reserved_seats')  # Add this
    seat = relationship('Seat', back_populates='reserved_seats')  # Add this


if __name__ == '__main__':
    engine = create_engine('sqlite:///cinema.db')
    Base.metadata.create_all(engine)
