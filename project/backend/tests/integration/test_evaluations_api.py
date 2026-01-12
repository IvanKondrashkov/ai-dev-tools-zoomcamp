import pytest
from fastapi import status
from app.models import Resume, Evaluation


def test_create_evaluation(client, db_session):
    """Test creating an evaluation."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    evaluation_data = {
        "resume_id": resume.id,
        "rating": 4.5,
        "comment": "Great candidate",
        "evaluator_name": "HR Manager"
    }

    response = client.post("/api/evaluations/", json=evaluation_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["rating"] == 4.5
    assert data["comment"] == "Great candidate"
    assert data["evaluator_name"] == "HR Manager"
    assert data["resume_id"] == resume.id


def test_create_evaluation_invalid_rating(client, db_session):
    """Test creating an evaluation with invalid rating."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    evaluation_data = {
        "resume_id": resume.id,
        "rating": 6.0,  # Invalid: > 5.0
        "evaluator_name": "HR Manager"
    }

    response = client.post("/api/evaluations/", json=evaluation_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_evaluation_resume_not_found(client):
    """Test creating an evaluation for non-existent resume."""
    evaluation_data = {
        "resume_id": 999,
        "rating": 4.0,
        "evaluator_name": "HR Manager"
    }

    response = client.post("/api/evaluations/", json=evaluation_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Resume not found" in response.json()["detail"]


def test_get_evaluations_for_resume(client, db_session):
    """Test getting all evaluations for a resume."""
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
        comment="Excellent",
        evaluator_name="Manager 2"
    )
    db_session.add(eval1)
    db_session.add(eval2)
    db_session.commit()

    response = client.get(f"/api/evaluations/resume/{resume.id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["rating"] in [4.0, 5.0]
    assert data[1]["rating"] in [4.0, 5.0]


def test_get_evaluations_empty(client, db_session):
    """Test getting evaluations for resume with none."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    response = client.get(f"/api/evaluations/resume/{resume.id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_get_evaluation_by_id(client, db_session):
    """Test getting a specific evaluation by ID."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    evaluation = Evaluation(
        resume_id=resume.id,
        rating=4.5,
        comment="Test comment",
        evaluator_name="Test Evaluator"
    )
    db_session.add(evaluation)
    db_session.commit()

    response = client.get(f"/api/evaluations/{evaluation.id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == evaluation.id
    assert data["rating"] == 4.5
    assert data["comment"] == "Test comment"


def test_get_evaluation_not_found(client):
    """Test getting a non-existent evaluation."""
    response = client.get("/api/evaluations/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

