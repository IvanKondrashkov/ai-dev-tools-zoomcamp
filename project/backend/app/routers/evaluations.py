from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Evaluation, Resume
from app.schemas import EvaluationCreate, EvaluationResponse

router = APIRouter()


@router.post("/", response_model=EvaluationResponse, status_code=201)
async def create_evaluation(
    evaluation: EvaluationCreate,
    db: Session = Depends(get_db)
):
    """Create a new evaluation for a resume."""
    # Check if resume exists
    resume = db.query(Resume).filter(Resume.id == evaluation.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db_evaluation = Evaluation(
        resume_id=evaluation.resume_id,
        rating=evaluation.rating,
        comment=evaluation.comment,
        evaluator_name=evaluation.evaluator_name
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)

    return db_evaluation


@router.get("/resume/{resume_id}", response_model=List[EvaluationResponse])
async def get_resume_evaluations(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Get all evaluations for a specific resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    evaluations = db.query(Evaluation).filter(
        Evaluation.resume_id == resume_id
    ).order_by(Evaluation.created_at.desc()).all()

    return evaluations


@router.get("/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific evaluation by ID."""
    evaluation = db.query(Evaluation).filter(
        Evaluation.id == evaluation_id
    ).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

