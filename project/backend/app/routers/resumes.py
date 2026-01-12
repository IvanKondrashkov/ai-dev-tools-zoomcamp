from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import aiofiles
from PyPDF2 import PdfReader
from app.database import get_db
from app.models import Resume
from app.schemas import ResumeResponse, ResumeListResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract text content from PDF or TXT file."""
    try:
        if file_type.lower() == "pdf":
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        elif file_type.lower() == "txt":
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                return await f.read()
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


@router.post("/", response_model=ResumeResponse, status_code=201)
async def create_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a new resume file (PDF or TXT)."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # Validate file type
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Extract text content
    content = await extract_text_from_file(file_path, file_extension)

    # Create database record
    db_resume = Resume(
        filename=file.filename,
        original_filename=file.filename,
        file_type=file_extension,
        file_path=file_path,
        content=content
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    return db_resume


@router.get("/", response_model=ResumeListResponse)
async def list_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all resumes."""
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    total = db.query(Resume).count()
    return ResumeListResponse(resumes=resumes, total=total)


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific resume by ID."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: int,
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Update a resume (replace file)."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if file:
        # Validate file type
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ["pdf", "txt"]:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are allowed"
            )

        # Delete old file
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)

        # Save new file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        # Extract text content
        content = await extract_text_from_file(file_path, file_extension)

        # Update database record
        resume.filename = file.filename
        resume.original_filename = file.filename
        resume.file_type = file_extension
        resume.file_path = file_path
        resume.content = content

    db.commit()
    db.refresh(resume)
    return resume


@router.delete("/{resume_id}", status_code=204)
async def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Delete a resume and its file."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Delete file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    # Delete database record (cascade will handle related records)
    db.delete(resume)
    db.commit()
    return None

