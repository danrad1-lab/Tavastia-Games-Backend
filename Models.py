from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from Datebase import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)

    seats = relationship("Seat", back_populates="user")


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    seat_number = Column(Integer, unique=True)
    is_booked = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="seats")






