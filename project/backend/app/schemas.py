from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ResumeBase(BaseModel):
    filename: str
    original_filename: str
    file_type: str
    content: Optional[str] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeResponse(ResumeBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResumeListResponse(BaseModel):
    resumes: List[ResumeResponse]
    total: int


class EvaluationBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None
    evaluator_name: str


class EvaluationCreate(EvaluationBase):
    resume_id: int


class EvaluationResponse(EvaluationBase):
    id: int
    resume_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessageBase(BaseModel):
    message: str
    username: str


class ChatMessageCreate(ChatMessageBase):
    resume_id: int


class ChatMessageResponse(ChatMessageBase):
    id: int
    resume_id: int
    created_at: datetime

    class Config:
        from_attributes = True

