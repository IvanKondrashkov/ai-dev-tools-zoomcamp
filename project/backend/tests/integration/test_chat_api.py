import pytest
from fastapi import status
from app.models import Resume, ChatMessage


def test_get_chat_messages(client, db_session):
    """Test getting chat messages for a resume."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    msg1 = ChatMessage(
        resume_id=resume.id,
        username="User1",
        message="First message"
    )
    msg2 = ChatMessage(
        resume_id=resume.id,
        username="User2",
        message="Second message"
    )
    db_session.add(msg1)
    db_session.add(msg2)
    db_session.commit()

    response = client.get(f"/api/chat/resume/{resume.id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] in ["User1", "User2"]
    assert data[1]["username"] in ["User1", "User2"]


def test_get_chat_messages_empty(client, db_session):
    """Test getting chat messages when none exist."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    response = client.get(f"/api/chat/resume/{resume.id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_get_chat_messages_resume_not_found(client):
    """Test getting chat messages for non-existent resume."""
    response = client.get("/api/chat/resume/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Resume not found" in response.json()["detail"]

