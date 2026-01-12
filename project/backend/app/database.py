from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL is the primary database
# For local development without Docker, use: postgresql://user:password@localhost:5432/resume_review
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://resume_review:resume_review_password@localhost:5432/resume_review"
)

# Create engine with connection pooling for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

