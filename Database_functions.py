from sqlalchemy.sql.functions import user

from Datebase import SessionLocal
from Models import User, Seat



def get_all_seats():
    with SessionLocal() as db:
        seats = db.query(Seat).order_by(Seat.id).all()
        return seats



def get_seat(seat_id: int):
    with SessionLocal() as db:
        return db.query(Seat).filter_by(id=seat_id).first()


def seat_booking(user: User):
    with SessionLocal() as db:
        seat = db.query(Seat).filter_by(id=user.id).first()

        if not seat:
            return {"error": "Seat not found"}

        if seat.is_booked:
            return {"error": "Seat already booked"}

        seat.is_booked = True

        seat.user_id = user.id

        db.commit()

        return {"status": "Seat booked"}




def get_user(user_id: int):
    with SessionLocal() as db:
        return db.query(User).filter_by(id=user_id).first()


def set_user(user: User):
    with SessionLocal() as db:
        db.add(user)

        db.commit()

        db.refresh(user)

    return user

def delete_booking(seat_id: int):
    with SessionLocal() as db:
        seat = db.query(Seat).filter_by(id=seat_id).first()
        if not seat:
            return {"error": "Seat not found"}

        if not seat.user_id:
            return {"error": "No user assigned to this seat"}

        user = db.query(User).filter_by(id=seat.user_id).first()
        if not user:
            return {"error": "User not found"}

        # теперь безопасно изменять
        seat.is_booked = False
        seat.user_id = None

        db.delete(user)
        db.commit()

        return {"message": "Booking deleted successfully"}