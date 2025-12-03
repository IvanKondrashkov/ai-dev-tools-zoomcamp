"""
Integration tests for API endpoints.
These tests require a running database.
"""
import pytest
import pytest_asyncio
import httpx
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from main import app
from database import get_db


@pytest_asyncio.fixture
async def client(db):
    """Create an async test client with overridden database dependency"""
    # Override the get_db dependency to use test database
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_session_integration(client, setup_db):
    """Integration test for creating a session"""
    response = await client.post("/api/sessions")
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
    create_response = await client.post("/api/sessions")
    session_id = create_response.json()["session_id"]
    
    # Get the session
    response = await client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_session_not_found_integration(client, setup_db):
    """Integration test for getting non-existent session"""
    response = await client.get("/api/sessions/nonexistent-session-id")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_code_javascript_integration(client, setup_db):
    """Integration test for JavaScript code execution"""
    response = await client.post(
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
    response = await client.post(
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
    response = await client.post(
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
    response = await client.post(
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
    response = await client.post(
        "/api/execute",
        json={"code": "print('test')", "language": "invalid"},
    )
    assert response.status_code == 400
