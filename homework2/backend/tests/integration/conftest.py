import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database import Base
import os


def get_test_database_url():
    """Get test database URL"""
    raw_test_url = os.getenv(
        "DATABASE_URL",
        "postgresql://test_user:test_password@localhost:5432/test_db"
    )
    
    # Ensure asyncpg driver is used
    if raw_test_url.startswith("postgres://"):
        raw_test_url = raw_test_url.replace("postgres://", "postgresql://", 1)
    
    if raw_test_url.startswith("postgresql://") and "+asyncpg" not in raw_test_url:
        return raw_test_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        return raw_test_url


@pytest_asyncio.fixture(scope="function")
async def setup_db():
    """Setup test database - create/drop tables for each test"""
    test_database_url = get_test_database_url()
    
    # Create engine for setup
    engine = create_async_engine(
        test_database_url,
        echo=False,
        poolclass=None,
    )
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        # Cleanup after test
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db(setup_db):
    """Get test database session for each test"""
    test_database_url = get_test_database_url()
    
    # Create engine for this test
    engine = create_async_engine(
        test_database_url,
        echo=False,
        poolclass=None,
    )
    
    TestSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    try:
        async with TestSessionLocal() as session:
            yield session
            await session.rollback()
    finally:
        await engine.dispose()
