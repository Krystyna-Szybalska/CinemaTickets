import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, User, Movie, Hall, Seat, Showing, Reservation, ReservedSeat


# Connect to the database
engine = create_engine('sqlite:///../cinema.db')
Session = sessionmaker(bind=engine)
session = Session()

# Delete data from all tables
session.query(ReservedSeat).delete()
session.query(Reservation).delete()
session.query(Showing).delete()
session.query(Seat).delete()
session.query(Hall).delete()
session.query(Movie).delete()
session.query(User).delete()

# Commit the changes
session.commit()

print("All data has been deleted.")