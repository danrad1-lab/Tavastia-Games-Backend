from Models import Seat, User
from Database_functions import get_all_seats, seat_booking, set_user, delete_booking, seat_check
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from jwt_and_email import send_email, create_token, verify_token
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

class TokenRequest(BaseModel):
    token: str

class DeleteRequest(BaseModel):
    seat_id: int
    password: str

    class Config:
        from_attributes = True


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
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
def created_booking(booking_requst: BookingRequest):

    user = User(
        id=booking_requst.seat_id,
        first_name=booking_requst.first_name,
        last_name=booking_requst.last_name,
        email=booking_requst.email,
    )
    if seat_check(user):
        token = create_token(user.id, user.first_name, user.last_name, user.email)
        try:
            send_email(user.email, token)
        except Exception as e:
            return {"message": "Something went wrong with email sending"}
    
        return {"message": "Check your email"}
        
    return {"message": "Something went wrong"}



@app.post("/book_seat")
def confirm_booking(tokenrequest: TokenRequest):
    data = verify_token(tokenrequest.token)

    if not data:
        return {"error": "Invalid or expired token"}
    
    user = User(
        id=data.get("id"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email")
    )
    if seat_check(user): # seat_check return true if place is free.
        set_user(user)
        return seat_booking(user)

    return {"message": "Something went wrong with seat booking"}



@app.post("/delete_booking")
def delete_book(delete_request: DeleteRequest):
    if delete_request.password != PASSWORD:
        return {"error": "Wrong password"}

    return delete_booking(delete_request.seat_id)

