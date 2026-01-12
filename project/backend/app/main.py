from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resumes, chat, evaluations
from app.database import engine, Base
import os

app = FastAPI(
    title="HR Resume Review Platform",
    description="Backend API for HR resume evaluation and review platform",
    version="1.0.0",
    # OpenAPI specification is defined in openapi.yaml at project root
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resumes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(evaluations.router, prefix="/api/evaluations", tags=["evaluations"])


@app.get("/")
async def root():
    return {"message": "HR Resume Review Platform API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup."""
    # Only create tables if not in test mode
    if os.getenv("ENVIRONMENT") != "test":
        Base.metadata.create_all(bind=engine)

