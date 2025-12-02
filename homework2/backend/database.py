import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, DateTime, Integer, func
from typing import AsyncGenerator

# Database URL from environment or construct from POSTGRES_* variables
raw_url = os.getenv("DATABASE_URL")
if not raw_url:
    # Build DATABASE_URL from POSTGRES_* environment variables (fallback)
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_user = os.getenv("POSTGRES_USER", "coding_interview")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "coding_interview_password")
    postgres_db = os.getenv("POSTGRES_DB", "coding_interview_db")
    raw_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

# Ensure asyncpg driver is used
if raw_url.startswith("postgresql://") and "+asyncpg" not in raw_url:
    DATABASE_URL = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = raw_url

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


# Database models
class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String(255), primary_key=True)
    code = Column(Text, nullable=False, default="")
    language = Column(String(50), nullable=False, default="javascript")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CodeHistory(Base):
    __tablename__ = "code_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())


# Dependency for getting database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

