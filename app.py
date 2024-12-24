import json
from collections import defaultdict

from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from crud import get_showings, get_available_seats, create_reservation
from auth import hash_password, verify_password, create_token
from fastapi import Header
from auth import decode_token
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Showing
from datetime import datetime, timedelta, timezone
from fastapi.logger import logger

app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.user_id)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"message": "Access granted", "user_id": user_id}


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/showings", response_model=dict)
async def get_showings(db: Session = Depends(get_db)):
    logger.info("Fetching showings data")
    today = datetime.now(timezone.utc)
    upcoming_dates = [today + timedelta(days=i) for i in range(3)]
    logger.info(f"Dates being fetched: {upcoming_dates}")
    try:
        showings_query = (
            db.query(Showing)
            .filter(Showing.showing_date >= today)
            .order_by(Showing.showing_date)
            .all()
        )
        logger.info(f"Fetched {len(showings_query)} showings")

        # Group showings
        grouped_showings = defaultdict(lambda: defaultdict(list))
        for showing in showings_query:
            showing_date = showing.showing_date.date()
            grouped_showings[showing_date][showing.movie.title].append(
                showing.showing_date.time().strftime("%H:%M")
            )

        result = {
            date.strftime("%d.%m.%Y"): {
                movie: ", ".join(times) for movie, times in movies.items()
            }
            for date, movies in grouped_showings.items()
        }

        logger.info("Successfully generated response data")
        # to nie zwraca JSONA a powinno todo
        return result
    except Exception as e:
        logger.error(f"Error fetching showings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/test", response_class=HTMLResponse)
async def test_page():
    return "<h1>Test Page Loaded</h1>"


@app.get("/reserve/{showing_id}")
async def reserve(request: Request, showing_id: str, db: Session = Depends(get_db)):
    seats = get_available_seats(db, showing_id)
    return templates.TemplateResponse("reserve.html", {"request": request, "showing_id": showing_id, "seats": seats})


@app.post("/reserve/{showing_id}")
async def confirm_reservation(request: Request, showing_id: str, db: Session = Depends(get_db)):
    # Example: Reserve seats (seat IDs will come from the form data)
    form = await request.form()
    selected_seats = form.getlist("seats")  # Get selected seats from form
    create_reservation(db, showing_id, selected_seats)  # Save reservation to DB
    return templates.TemplateResponse("confirmation.html", {"request": request})
