from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import socketio
import uuid
import os
import asyncio
from typing import Dict, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from code_executor import execute_code_server
from database import get_db, engine, Base, AsyncSessionLocal
from db_service import (
    create_session,
    get_session,
    update_session_code,
    update_session_language,
    get_or_create_session,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup - wait for database to be ready
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"Failed to connect to database after {max_retries} attempts: {e}")
                raise
    
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Coding Interview Platform API",
    description="API for collaborative coding interview platform",
    version="1.0.0",
    lifespan=lifespan,
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(
    cors_allowed_origins=cors_origins,
    async_mode="asgi",
)
socket_app = socketio.ASGIApp(sio, app)


class SessionResponse(BaseModel):
    session_id: str


class ExecuteRequest(BaseModel):
    code: str
    language: str


class ExecuteResponse(BaseModel):
    output: Optional[str] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str


@app.post("/api/sessions", response_model=SessionResponse, status_code=201)
async def create_session_endpoint(db: AsyncSession = Depends(get_db)):
    session_id = await create_session(db)
    return SessionResponse(session_id=session_id)


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session_endpoint(session_id: str, db: AsyncSession = Depends(get_db)):
    session = await get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(session_id=session_id)


@app.post("/api/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    if request.language not in ["javascript", "python", "go", "java"]:
        raise HTTPException(
            status_code=400, detail="Unsupported language"
        )
    
    # JavaScript and Python execute in browser
    if request.language in ["javascript", "python"]:
        return ExecuteResponse(
            output="Code execution happens in the browser. This endpoint is for API compatibility.",
            error=None,
        )
    
    # Go and Java execute on server
    if request.language in ["go", "java"]:
        try:
            output, error = await execute_code_server(
                request.code,
                request.language,
                timeout=10
            )
            return ExecuteResponse(
                output=output,
                error=error,
            )
        except Exception as e:
            return ExecuteResponse(
                output=None,
                error=f"Server execution error: {str(e)}",
            )
    
    return ExecuteResponse(
        output=None,
        error="Unsupported language for server execution",
    )


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.event
async def join_session(sid, data):
    session_id = data.get("session_id")
    async with AsyncSessionLocal() as db:
        session = await get_or_create_session(db, session_id)
        await sio.enter_room(sid, session_id)
        await sio.emit(
            "code_update",
            {
                "session_id": session_id,
                "code": session["code"],
                "language": session["language"],
            },
            room=sid,
        )


@sio.event
async def code_change(sid, data):
    session_id = data.get("session_id")
    code = data.get("code", "")
    
    async with AsyncSessionLocal() as db:
        session = await get_or_create_session(db, session_id)
        await update_session_code(db, session_id, code)
        await sio.emit(
            "code_update",
            {
                "session_id": session_id,
                "code": code,
                "language": session["language"],
            },
            room=session_id,
            skip_sid=sid,
        )


@sio.event
async def language_change(sid, data):
    session_id = data.get("session_id")
    language = data.get("language")
    
    async with AsyncSessionLocal() as db:
        session = await get_or_create_session(db, session_id)
        await update_session_language(db, session_id, language)
        await sio.emit(
            "language_update",
            {
                "session_id": session_id,
                "language": language,
            },
            room=session_id,
            skip_sid=sid,
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)

