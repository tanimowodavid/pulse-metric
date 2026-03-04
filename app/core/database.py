from sqlalchemy import create_url, create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base


DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/pulse_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
