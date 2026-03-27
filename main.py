from Models import Seat, User
from Database_functions import get_all_seats, seat_booking, set_user, delete_booking
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


class BookingRequest(BaseModel):
    seat_id: int
    first_name: str
    last_name: str
    email: str

class SeatResponse(BaseModel):
    id: int
    seat_number: int
    is_booked: bool

    class Config:
        from_attributes = True


class DeleteRequest(BaseModel):
    seat_id: int
    password: str

    class Config:
        from_attributes = True


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.tavastiagames.com",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


PASSWORD = "123456789"
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/seats", response_model = list[SeatResponse])
def get_seats():
    return get_all_seats()

@app.post("/booking")
def book_seat(booking_requst: BookingRequest):

    user = User(
        id=booking_requst.seat_id,
        first_name=booking_requst.first_name,
        last_name=booking_requst.last_name,
        email=booking_requst.email,
    )

    set_user(user)

    return seat_booking(user)

@app.post("/delete_booking")
def delete_book(delete_request: DeleteRequest):
    if delete_request.password != PASSWORD:
        return {"error": "Wrong password"}

    return delete_booking(delete_request.seat_id)

