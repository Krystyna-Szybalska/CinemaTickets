import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from models import Base, Hall, Seat

# Connect to the database
engine = create_engine('sqlite:///../cinema.db')
Session = sessionmaker(bind=engine)
session = Session()

# Lists all tables
inspector = inspect(engine)
print(inspector.get_table_names())

# Query halls
halls = session.query(Hall).all()

# Display data
for hall in halls:
    print(f"Hall ID: {hall.hall_id}, Name: {hall.name}")

    # Query seats for the current hall
    seats = session.query(Seat).filter_by(hall_id=hall.hall_id).order_by(Seat.row_number, Seat.seat_number).all()

    # Organize seats by rows
    rows = {}
    for seat in seats:
        if seat.row_number not in rows:
            rows[seat.row_number] = []
        rows[seat.row_number].append(seat.seat_number)

    # Display rows of seats
    for row_number, seat_numbers in sorted(rows.items()):
        seat_line = " ".join([f"{seat:02d}" for seat in seat_numbers])
        print(f"  Row {row_number}: {seat_line}")

print("All hall and seat data has been displayed.")