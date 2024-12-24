from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Hall, Seat, Movie, Showing
import pandas as pd
from datetime import datetime, timedelta
import random

engine = create_engine('sqlite:///cinema.db')
Session = sessionmaker(bind=engine)
session = Session()


def add_halls_and_seats():
    """
    Insert data for halls and seats
    """

    # Data for halls
    halls_data = [
        {"name": "Houston", "rows": 8, "seats_per_row": 8},  # 64 seats
        {"name": "Dallas", "rows": 8, "seats_per_row": 16},  # 128 seats
        {"name": "Chicago", "rows": 8, "seats_per_row": 16},  # 128 seats
        {"name": "Philadelphia", "rows": 8, "seats_per_row": 16},  # 128 seats
        {"name": "Seattle", "rows": 16, "seats_per_row": 16},  # 256 seats
    ]

    # Insert halls and seats
    for hall_data in halls_data:
        # Create Hall
        hall = Hall(name=hall_data["name"])
        session.add(hall)
        session.flush()  # Ensure hall_id is generated before inserting seats

        # Generate seats
        for row in range(1, hall_data["rows"] + 1):  # Rows start at 1
            for seat in range(1, hall_data["seats_per_row"] + 1):  # Seats start at 1
                seat_entry = Seat(hall_id=hall.hall_id, row_number=row, seat_number=seat)
                session.add(seat_entry)

    print("Halls and seats generated and added to the session successfully.")


def add_movies():
    csv_path = "./kaggle_datasets/movies-performance-and-feature-statistics/movies.csv"

    # Load both datasets
    try:
        movies_data = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        exit()

    # Normalize column names (trim spaces)
    movies_data.columns = movies_data.columns.str.strip()

    # Iterate through each row and insert data into the Movies table
    for index, row in movies_data.iterrows():
        try:
            # Extract data from the main dataset
            title = row['Title']
            genre = row['Genre']
            duration = row['Runtime']
            rating = row['MPAA Rating']
            vote_average = row['Rating']
            release_date_str = row['Release Date']

            # Skip rows with missing critical data
            if pd.isna(title) or pd.isna(duration) or pd.isna(rating) or pd.isna(vote_average):
                # print(f"Skipping row {index} due to missing essential data.")
                continue

            release_date = None
            if release_date_str and not pd.isna(release_date_str):
                try:
                    release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()  # Convert string to date
                except ValueError:
                    # print(f"Invalid date format for movie {row['title']}: {release_date_str}")
                    pass

            # Calculate ticket price
            ticket_price = float(vote_average) * 5
            if ticket_price == 0:
                ticket_price = 25.0

            # Create a Movie object
            movie = Movie(
                title=title,
                genre=genre,
                duration_minutes=int(duration),
                rating=rating,
                ticket_price=ticket_price,
                release_date=release_date
            )

            # Add to the session
            session.add(movie)
        except Exception as e:
            # print(f"Skipping row {index} due to an error: {e}")
            pass

    print(f"Movies generated and added to the session successfully.")


def add_showings():
    # Define the start and end dates
    start_date = datetime(2024, 12, 1)  # Start date: 01.12.2024
    end_date = datetime(2025, 12, 31)  # End date: 31.12.2025
    date_range = (end_date - start_date).days  # Total days: 396

    # Define the showtimes for each day
    show_times = ['08:00', '11:00', '14:00', '17:00', '20:00']

    # Fetch all halls and movies from the database
    halls = session.query(Hall).all()
    movies = session.query(Movie).all()

    # Create showings for each day in the timespan
    for day_offset in range(date_range + 1):
        # Calculate the date for this loop
        current_date = start_date + timedelta(days=day_offset)

        # For each hall, create showings at 5 different times
        for hall in halls:
            for show_time in show_times:
                # Generate the showing datetime
                showing_datetime = datetime.combine(current_date, datetime.strptime(show_time, '%H:%M').time())

                # Randomly select a movie
                random_movie = random.choice(movies)

                # Create the showing record
                showing = Showing(
                    movie_id=random_movie.movie_id,
                    hall_id=hall.hall_id,
                    showing_date=showing_datetime
                )

                # Add the showing to the session
                session.add(showing)

    print("Showings generated and added to the session successfully.")


add_halls_and_seats()
add_movies()
add_showings()

# Commit the session to insert data
try:
    session.commit()
    print(f"Data has been successfully added to the database.")

except Exception as e:
    session.rollback()
    print(f"Error committing the halls and seats: {e}")
