from datetime import datetime, timedelta

from fastapi import Depends
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from auth import verify_password
from auth import hash_password
from database import get_db
from models import User, Showing, Seat, ReservedSeat, Reservation
from schemas import ReservationRequest, ShowingDetailResponse, ShowingResponse, UserResponse, \
    LoginRequest, RegisterRequest, SeatResponse

app = FastAPI()

origins = [
    "https://localhost:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/register", response_model=UserResponse)
async def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(request.password)

        new_user = User(email=request.email, password=hashed_password, phone_number=request.phone_number,
                        name=request.name)
        db.add(new_user)
        db.commit()

        return UserResponse(user_id=new_user.user_id, email=new_user.email, name=new_user.name)

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/login", response_model=UserResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return UserResponse(user_id=user.user_id, email=user.email, name=user.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/showings")
async def get_showings(
        start_date: datetime = None,
        end_date: datetime = None,
        db: Session = Depends(get_db)
):
    # If no start date is provided, default to today
    if start_date is None:
        start_date = datetime.now()

    # If no end date is provided, default to 3 days after the start date
    if end_date is None:
        end_date = start_date + timedelta(days=1)
    try:
        showings = db.query(Showing).filter(Showing.showing_date.between(start_date, end_date)).all()
        if not showings:
            raise HTTPException(status_code=404, detail="No showings found in the given time range")

        return [ShowingResponse(
            showing_id=showing.showing_id,
            movie_title=showing.movie.title,
            showing_date=showing.showing_date,
            hall_id=showing.hall_id,
            hall_name=showing.hall.name
        ) for showing in showings]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/showing/{showing_id}", response_model=ShowingDetailResponse)
async def get_showing_details(showing_id: str, db: Session = Depends(get_db)):
    # Fetch the showing details
    showing = db.query(Showing).filter(Showing.showing_id == showing_id).first()
    if not showing:
        raise HTTPException(status_code=404, detail="Showing not found")

    # Fetch hall related to the showing
    hall = showing.hall

    # Get all seats in the hall
    seats = db.query(Seat).filter(Seat.hall_id == hall.hall_id).all()

    # Get the list of seat IDs that are already reserved for this showing
    reserved_seat_ids = db.query(ReservedSeat.seat_id).join(Reservation).filter(
        Reservation.showing_id == showing_id
    ).all()

    reserved_seat_ids = [reserved_seat.seat_id for reserved_seat in reserved_seat_ids]

    # Filter out the reserved seats from the available seats
    available_seats = [
        SeatResponse(
            seat_id=seat.seat_id,
            seat_number=seat.seat_number,
            row_number=seat.row_number,
            is_reserved=seat.seat_id in reserved_seat_ids
        )
        for seat in seats
    ]

    # Return showing details, including available seats
    return ShowingDetailResponse(
        showing_id=showing.showing_id,
        movie=showing.movie.title,
        showing_date=showing.showing_date,
        hall_name=hall.name,
        available_seats=available_seats
    )


@app.post("/reserve")
async def create_reservation(reservation_request: ReservationRequest, db: Session = Depends(get_db)):
    try:
        showing = db.query(Showing).filter(Showing.showing_id == reservation_request.showing_id).first()
        if not showing:
            raise HTTPException(status_code=404, detail="Showing not found")

        seats = db.query(Seat).filter(Seat.seat_id.in_(reservation_request.seat_ids)).all()
        if len(seats) != len(reservation_request.seat_ids):
            raise HTTPException(status_code=404, detail="Some seats not found")

        # Create reservation
        reservation = Reservation(user_id=reservation_request.user_id, showing_id=reservation_request.showing_id,
                                  reservation_date=datetime.now())
        db.add(reservation)
        db.commit()

        # Reserve seats
        reserved_seats = [
            ReservedSeat(reservation_id=reservation.reservation_id, seat_id=seat.seat_id, ticket_type="Standard",
                         ticket_price=10.0) for seat in seats]
        db.add_all(reserved_seats)
        db.commit()

        return {"message": "Reservation successful", "reservation_id": reservation.reservation_id}

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
