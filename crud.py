# Database operations (e.g., create_user, authenticate_user)
from sqlalchemy.orm import Session
from models import User, Showing, Seat, ReservedSeat, Reservation
from auth import hash_password


def create_user(db: Session, name: str, email: str, password: str):
    db_user = User(name=name, email=email, password=hash_password(password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_showings(db: Session):
    return db.query(Showing).all()


def get_available_seats(db: Session, showing_id: str):
    # Find all seats in the hall of the specified showing
    showing = db.query(Showing).filter(Showing.showing_id == showing_id).first()

    # If the showing does not exist, return an empty list
    if not showing:
        return []

    # Get all seats in the hall of the showing
    hall_seats = db.query(Seat).filter(Seat.hall_id == showing.hall_id).all()

    # Get all reserved seat IDs for this showing
    reserved_seat_ids = (
        db.query(ReservedSeat.seat_id)
        .join(Reservation)
        .filter(Reservation.showing_id == showing_id)
        .all()
    )
    reserved_seat_ids = [seat_id for seat_id, in reserved_seat_ids]

    # Filter out reserved seats
    available_seats = [seat for seat in hall_seats if seat.seat_id not in reserved_seat_ids]

    return available_seats


def create_reservation(db: Session, showing_id: str, seat_ids: list):
    # Add reservation and associate seats
    # Implement logic to add a reservation to the DB
    pass
