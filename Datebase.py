from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres123:ipmbiwT6rTg9nzN13uZKccVz2mpTjj2W@dpg-d732ne24d50c73fg7jog-a/tavastiagames"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

