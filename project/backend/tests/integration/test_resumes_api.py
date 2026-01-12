import pytest
import io
from fastapi import status
from app.models import Resume


def test_create_resume_pdf(client, upload_dir):
    """Test creating a resume with PDF file."""
    file_content = b"%PDF-1.4\nTest PDF content"
    files = {"file": ("test_resume.pdf", io.BytesIO(file_content), "application/pdf")}
    
    response = client.post("/api/resumes/", files=files)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["filename"] == "test_resume.pdf"
    assert data["file_type"] == "pdf"
    assert "id" in data


def test_create_resume_txt(client, upload_dir):
    """Test creating a resume with TXT file."""
    file_content = b"Resume content in text format"
    files = {"file": ("resume.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.post("/api/resumes/", files=files)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["filename"] == "resume.txt"
    assert data["file_type"] == "txt"


def test_create_resume_invalid_file_type(client, upload_dir):
    """Test creating a resume with invalid file type."""
    file_content = b"Some content"
    files = {"file": ("document.doc", io.BytesIO(file_content), "application/msword")}
    
    response = client.post("/api/resumes/", files=files)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only PDF and TXT files are allowed" in response.json()["detail"]


def test_list_resumes_empty(client):
    """Test listing resumes when none exist."""
    response = client.get("/api/resumes/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert len(data["resumes"]) == 0


def test_list_resumes_with_data(client, upload_dir, db_session):
    """Test listing resumes with existing data."""
    # Create test resumes
    resume1 = Resume(
        filename="resume1.pdf",
        original_filename="resume1.pdf",
        file_type="pdf",
        file_path="/uploads/resume1.pdf"
    )
    resume2 = Resume(
        filename="resume2.txt",
        original_filename="resume2.txt",
        file_type="txt",
        file_path="/uploads/resume2.txt"
    )
    db_session.add(resume1)
    db_session.add(resume2)
    db_session.commit()

    response = client.get("/api/resumes/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 2
    assert len(data["resumes"]) == 2


def test_get_resume_by_id(client, db_session):
    """Test getting a specific resume by ID."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf",
        content="Test content"
    )
    db_session.add(resume)
    db_session.commit()

    response = client.get(f"/api/resumes/{resume.id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == resume.id
    assert data["filename"] == "test.pdf"
    assert data["content"] == "Test content"


def test_get_resume_not_found(client):
    """Test getting a non-existent resume."""
    response = client.get("/api/resumes/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Resume not found" in response.json()["detail"]


def test_update_resume(client, upload_dir, db_session):
    """Test updating a resume."""
    resume = Resume(
        filename="old.pdf",
        original_filename="old_resume.pdf",
        file_type="pdf",
        file_path="/uploads/old.pdf"
    )
    db_session.add(resume)
    db_session.commit()

    file_content = b"Updated content"
    files = {"file": ("new_resume.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.put(f"/api/resumes/{resume.id}", files=files)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["filename"] == "new_resume.txt"
    assert data["file_type"] == "txt"


def test_delete_resume(client, db_session):
    """Test deleting a resume."""
    resume = Resume(
        filename="test.pdf",
        original_filename="test_resume.pdf",
        file_type="pdf",
        file_path="/uploads/test.pdf"
    )
    db_session.add(resume)
    db_session.commit()
    resume_id = resume.id

    response = client.delete(f"/api/resumes/{resume_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(f"/api/resumes/{resume_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_resume_not_found(client):
    """Test deleting a non-existent resume."""
    response = client.delete("/api/resumes/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

