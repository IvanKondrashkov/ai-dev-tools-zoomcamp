"""
Integration tests for WebSocket functionality.
These tests require a running server and database.
"""
import pytest
import socketio
import asyncio
import sys
import os
import uuid

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import AsyncSessionLocal
from db_service import create_session, get_session


@pytest.fixture
async def test_session_id():
    """Create a test session in database"""
    async with AsyncSessionLocal() as db:
        session_id = await create_session(db)
        yield session_id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_websocket_connection_integration():
    """Integration test for WebSocket connection"""
    client = socketio.AsyncClient()
    try:
        await client.connect("http://localhost:8000", wait_timeout=5)
        assert client.connected
    finally:
        await client.disconnect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_join_session_integration(test_session_id):
    """Integration test for joining a session via WebSocket"""
    client = socketio.AsyncClient()
    try:
        await client.connect("http://localhost:8000", wait_timeout=5)
        
        received_data = {}
        
        @client.on("code_update")
        def on_code_update(data):
            received_data.update(data)
        
        await client.emit("join_session", {"session_id": test_session_id})
        await asyncio.sleep(0.5)
        
        assert "code" in received_data
        assert received_data.get("session_id") == test_session_id
    finally:
        await client.disconnect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_code_change_broadcast_integration(test_session_id):
    """Integration test for code change broadcast via WebSocket"""
    client1 = socketio.AsyncClient()
    client2 = socketio.AsyncClient()
    
    try:
        await client1.connect("http://localhost:8000", wait_timeout=5)
        await client2.connect("http://localhost:8000", wait_timeout=5)
        
        received_updates = []
        
        @client2.on("code_update")
        def on_code_update(data):
            received_updates.append(data)
        
        await client1.emit("join_session", {"session_id": test_session_id})
        await client2.emit("join_session", {"session_id": test_session_id})
        await asyncio.sleep(0.5)
        
        new_code = "updated code"
        await client1.emit(
            "code_change",
            {"session_id": test_session_id, "code": new_code},
        )
        await asyncio.sleep(0.5)
        
        assert len(received_updates) > 0
        assert any(update.get("code") == new_code for update in received_updates)
    finally:
        await client1.disconnect()
        await client2.disconnect()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_language_change_broadcast_integration(test_session_id):
    """Integration test for language change broadcast via WebSocket"""
    client1 = socketio.AsyncClient()
    client2 = socketio.AsyncClient()
    
    try:
        await client1.connect("http://localhost:8000", wait_timeout=5)
        await client2.connect("http://localhost:8000", wait_timeout=5)
        
        received_updates = []
        
        @client2.on("language_update")
        def on_language_update(data):
            received_updates.append(data)
        
        await client1.emit("join_session", {"session_id": test_session_id})
        await client2.emit("join_session", {"session_id": test_session_id})
        await asyncio.sleep(0.5)
        
        new_language = "python"
        await client1.emit(
            "language_change",
            {"session_id": test_session_id, "language": new_language},
        )
        await asyncio.sleep(0.5)
        
        assert len(received_updates) > 0
        assert any(
            update.get("language") == new_language for update in received_updates
        )
    finally:
        await client1.disconnect()
        await client2.disconnect()

