import pytest
from datetime import datetime
from app.models import Resume, Evaluation, ChatMessage


def test_resume_model_creation(db_session):
    """Test creating a Resume model."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf",
        content="Test resume content"
    )
    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    assert resume.id is not None
    assert resume.filename == "test.pdf"
    assert resume.original_filename == "test_resume.pdf"
    assert resume.file_type == "pdf"
    assert resume.content == "Test resume content"
    assert resume.created_at is not None


def test_evaluation_model_creation(db_session):
    """Test creating an Evaluation model."""
    # First create a resume
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    # Create evaluation
    evaluation = Evaluation(
        resume_id=resume.id,
        rating=4.5,
        comment="Great candidate",
        evaluator_name="HR Manager"
    )
    db_session.add(evaluation)
    db_session.commit()
    db_session.refresh(evaluation)

    assert evaluation.id is not None
    assert evaluation.resume_id == resume.id
    assert evaluation.rating == 4.5
    assert evaluation.comment == "Great candidate"
    assert evaluation.evaluator_name == "HR Manager"
    assert evaluation.created_at is not None


def test_chat_message_model_creation(db_session):
    """Test creating a ChatMessage model."""
    # First create a resume
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    # Create chat message
    message = ChatMessage(
        resume_id=resume.id,
        username="John Doe",
        message="This looks promising"
    )
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)

    assert message.id is not None
    assert message.resume_id == resume.id
    assert message.username == "John Doe"
    assert message.message == "This looks promising"
    assert message.created_at is not None


def test_resume_evaluation_relationship(db_session):
    """Test relationship between Resume and Evaluation."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    eval1 = Evaluation(
        resume_id=resume.id,
        rating=4.0,
        evaluator_name="Manager 1"
    )
    eval2 = Evaluation(
        resume_id=resume.id,
        rating=5.0,
        evaluator_name="Manager 2"
    )
    db_session.add(eval1)
    db_session.add(eval2)
    db_session.commit()

    db_session.refresh(resume)
    assert len(resume.evaluations) == 2
    assert resume.evaluations[0].rating == 4.0
    assert resume.evaluations[1].rating == 5.0


def test_resume_chat_messages_relationship(db_session):
    """Test relationship between Resume and ChatMessage."""
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
        message="Message 1"
    )
    msg2 = ChatMessage(
        resume_id=resume.id,
        username="User2",
        message="Message 2"
    )
    db_session.add(msg1)
    db_session.add(msg2)
    db_session.commit()

    db_session.refresh(resume)
    assert len(resume.chat_messages) == 2
    assert resume.chat_messages[0].message == "Message 1"
    assert resume.chat_messages[1].message == "Message 2"


def test_cascade_delete(db_session):
    """Test that deleting a resume cascades to evaluations and messages."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    eval1 = Evaluation(
        resume_id=resume.id,
        rating=4.0,
        evaluator_name="Manager"
    )
    msg1 = ChatMessage(
        resume_id=resume.id,
        username="User",
        message="Test message"
    )
    db_session.add(eval1)
    db_session.add(msg1)
    db_session.commit()

    resume_id = resume.id
    db_session.delete(resume)
    db_session.commit()

    # Check that related records are deleted
    assert db_session.query(Evaluation).filter_by(resume_id=resume_id).first() is None
    assert db_session.query(ChatMessage).filter_by(resume_id=resume_id).first() is None

