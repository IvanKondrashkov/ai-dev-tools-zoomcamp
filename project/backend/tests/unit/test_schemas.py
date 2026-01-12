import pytest
from pydantic import ValidationError
from app.schemas import (
    ResumeCreate,
    ResumeResponse,
    EvaluationCreate,
    EvaluationResponse,
    ChatMessageCreate,
    ChatMessageResponse
)


def test_resume_create_schema():
    """Test ResumeCreate schema validation."""
    resume = ResumeCreate(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        content="Test content"
    )
    assert resume.filename == "test.pdf"
    assert resume.file_type == "pdf"


def test_evaluation_create_schema_valid():
    """Test EvaluationCreate schema with valid data."""
    evaluation = EvaluationCreate(
        resume_id=1,
        rating=4.5,
        comment="Great candidate",
        evaluator_name="HR Manager"
    )
    assert evaluation.rating == 4.5
    assert evaluation.comment == "Great candidate"


def test_evaluation_create_schema_rating_too_low():
    """Test EvaluationCreate schema rejects rating below 1.0."""
    with pytest.raises(ValidationError):
        EvaluationCreate(
            resume_id=1,
            rating=0.5,
            evaluator_name="HR Manager"
        )


def test_evaluation_create_schema_rating_too_high():
    """Test EvaluationCreate schema rejects rating above 5.0."""
    with pytest.raises(ValidationError):
        EvaluationCreate(
            resume_id=1,
            rating=6.0,
            evaluator_name="HR Manager"
        )


def test_evaluation_create_schema_optional_comment():
    """Test EvaluationCreate schema with optional comment."""
    evaluation = EvaluationCreate(
        resume_id=1,
        rating=3.0,
        evaluator_name="HR Manager"
    )
    assert evaluation.comment is None


def test_chat_message_create_schema():
    """Test ChatMessageCreate schema validation."""
    message = ChatMessageCreate(
        resume_id=1,
        username="John Doe",
        message="Test message"
    )
    assert message.resume_id == 1
    assert message.username == "John Doe"
    assert message.message == "Test message"

