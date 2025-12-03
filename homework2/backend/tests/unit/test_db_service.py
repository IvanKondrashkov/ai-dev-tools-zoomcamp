"""
Unit tests for database service functions.
These tests mock the database session.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from db_service import (
    create_session,
    get_session,
    update_session_code,
    update_session_language,
    get_or_create_session,
)
from database import Session as SessionModel
import uuid


@pytest.fixture
def mock_db():
    """Create a mock database session"""
    db = AsyncMock(spec=AsyncSession)
    return db


@pytest.fixture
def mock_session():
    """Create a mock session object"""
    session = MagicMock()
    session.session_id = str(uuid.uuid4())
    session.code = "// Test code"
    session.language = "javascript"
    return session


@pytest.mark.asyncio
async def test_create_session(mock_db):
    """Test creating a new session"""
    session_id = await create_session(mock_db)
    
    assert isinstance(session_id, str)
    assert len(session_id) > 0
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_session_exists(mock_db, mock_session):
    """Test getting an existing session"""
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = mock_session
    
    mock_db.execute.return_value = result_mock
    
    session = await get_session(mock_db, mock_session.session_id)
    
    assert session is not None
    assert session["session_id"] == mock_session.session_id
    assert session["code"] == mock_session.code
    assert session["language"] == mock_session.language
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_session_not_exists(mock_db):
    """Test getting a non-existent session"""
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    
    mock_db.execute.return_value = result_mock
    
    session = await get_session(mock_db, "non-existent-id")
    
    assert session is None
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_session_code(mock_db):
    """Test updating session code"""
    result_mock = MagicMock()
    result_mock.rowcount = 1
    mock_db.execute.return_value = result_mock
    
    success = await update_session_code(mock_db, "test-session-id", "new code")
    
    assert success is True
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_session_code_not_found(mock_db):
    """Test updating code for non-existent session"""
    result_mock = MagicMock()
    result_mock.rowcount = 0
    mock_db.execute.return_value = result_mock
    
    success = await update_session_code(mock_db, "non-existent-id", "new code")
    
    assert success is False
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_session_language(mock_db):
    """Test updating session language"""
    result_mock = MagicMock()
    result_mock.rowcount = 1
    mock_db.execute.return_value = result_mock
    
    success = await update_session_language(mock_db, "test-session-id", "python")
    
    assert success is True
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_or_create_session_exists(mock_db, mock_session):
    """Test get_or_create_session when session exists"""
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = mock_session
    mock_db.execute.return_value = result_mock
    
    session = await get_or_create_session(mock_db, mock_session.session_id)
    
    assert session is not None
    assert session["session_id"] == mock_session.session_id
    mock_db.add.assert_not_called()


@pytest.mark.asyncio
async def test_get_or_create_session_not_exists(mock_db):
    """Test get_or_create_session when session doesn't exist"""
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = result_mock
    
    # Mock the refresh to set session attributes
    new_session = MagicMock()
    new_session.session_id = "new-session-id"
    new_session.code = "// Write your code here\n"
    new_session.language = "javascript"
    mock_db.refresh.return_value = None
    
    session = await get_or_create_session(mock_db, "new-session-id")
    
    assert session is not None
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()



