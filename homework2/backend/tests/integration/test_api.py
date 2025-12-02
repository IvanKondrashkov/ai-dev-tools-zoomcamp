"""
Integration tests for API endpoints.
These tests require a running database.
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from main import app
from database import engine, Base, AsyncSessionLocal
from db_service import create_session, get_session
import asyncio


@pytest.fixture(scope="function")
async def db_session():
    """Create a test database session"""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def setup_db():
    """Setup test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup can be added here if needed


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_session_integration(client, setup_db):
    """Integration test for creating a session"""
    response = client.post("/api/sessions")
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert isinstance(data["session_id"], str)
    assert len(data["session_id"]) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_session_integration(client, setup_db):
    """Integration test for getting a session"""
    # Create a session first
    create_response = client.post("/api/sessions")
    session_id = create_response.json()["session_id"]
    
    # Get the session
    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_session_not_found_integration(client, setup_db):
    """Integration test for getting non-existent session"""
    response = client.get("/api/sessions/nonexistent-session-id")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_code_javascript_integration(client, setup_db):
    """Integration test for JavaScript code execution"""
    response = client.post(
        "/api/execute",
        json={"code": "console.log('test');", "language": "javascript"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "output" in data or "error" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_code_python_integration(client, setup_db):
    """Integration test for Python code execution"""
    response = client.post(
        "/api/execute",
        json={"code": "print('test')", "language": "python"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "output" in data or "error" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_code_go_integration(client, setup_db):
    """Integration test for Go code execution"""
    code = """
package main

import "fmt"

func main() {
    fmt.Println("Hello from Go API!")
}
"""
    response = client.post(
        "/api/execute",
        json={"code": code, "language": "go"},
    )
    assert response.status_code == 200
    data = response.json()
    # If Go is not installed, we'll get an error message
    if data.get("error") and "not installed" in data["error"]:
        pytest.skip("Go is not installed on this system")
    assert "output" in data or "error" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_code_java_integration(client, setup_db):
    """Integration test for Java code execution"""
    code = """
System.out.println("Hello from Java API!");
"""
    response = client.post(
        "/api/execute",
        json={"code": code, "language": "java"},
    )
    assert response.status_code == 200
    data = response.json()
    # If Java is not installed, we'll get an error message
    if data.get("error") and "not installed" in data["error"]:
        pytest.skip("Java/JDK is not installed on this system")
    assert "output" in data or "error" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_code_invalid_language_integration(client, setup_db):
    """Integration test for invalid language"""
    response = client.post(
        "/api/execute",
        json={"code": "print('test')", "language": "invalid"},
    )
    assert response.status_code == 400

