import pytest
import os
import tempfile
import atexit

# Set test environment before importing app to prevent DB connection on import
os.environ["ENVIRONMENT"] = "test"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from typing import Generator
from app.database import Base, get_db
from app.main import app

# Create a temporary file for SQLite database (more reliable than in-memory)
_test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
_test_db_path = _test_db_file.name
_test_db_file.close()

TEST_DATABASE_URL = f"sqlite:///{_test_db_path}"

# Create engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def cleanup_test_db():
    """Clean up test database file on exit."""
    engine.dispose()
    if os.path.exists(_test_db_path):
        try:
            os.unlink(_test_db_path)
        except (PermissionError, OSError):
            pass  # File may be locked, ignore


atexit.register(cleanup_test_db)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create and drop tables for each test."""
    # Create all tables before test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after test
    Base.metadata.drop_all(bind=engine)
    # Close all connections before cleanup
    engine.dispose()


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def upload_dir(tmp_path):
    """Create a temporary upload directory for tests."""
    upload_path = tmp_path / "uploads"
    upload_path.mkdir()
    os.environ["UPLOAD_DIR"] = str(upload_path)
    yield str(upload_path)
    # Cleanup
    if "UPLOAD_DIR" in os.environ:
        del os.environ["UPLOAD_DIR"]

