from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
import json
from app.database import get_db, SessionLocal
from app.models import ChatMessage, Resume
from app.schemas import ChatMessageResponse

router = APIRouter()

# Store active WebSocket connections per resume
active_connections: Dict[int, List[WebSocket]] = {}


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, resume_id: int):
        await websocket.accept()
        if resume_id not in self.active_connections:
            self.active_connections[resume_id] = []
        self.active_connections[resume_id].append(websocket)

    def disconnect(self, websocket: WebSocket, resume_id: int):
        if resume_id in self.active_connections:
            self.active_connections[resume_id].remove(websocket)
            if not self.active_connections[resume_id]:
                del self.active_connections[resume_id]

    async def broadcast(self, message: dict, resume_id: int):
        if resume_id in self.active_connections:
            for connection in self.active_connections[resume_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error sending message: {e}")


manager = ConnectionManager()


@router.get("/resume/{resume_id}", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Get all chat messages for a specific resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    messages = db.query(ChatMessage).filter(
        ChatMessage.resume_id == resume_id
    ).order_by(ChatMessage.created_at.asc()).all()

    return messages


@router.websocket("/ws/{resume_id}")
async def websocket_endpoint(websocket: WebSocket, resume_id: int):
    """WebSocket endpoint for real-time chat."""
    # Verify resume exists
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            await websocket.close(code=1008, reason="Resume not found")
            return
    finally:
        db.close()

    await manager.connect(websocket, resume_id)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Validate message data
            if "username" not in message_data or "message" not in message_data:
                await websocket.send_json({
                    "error": "Username and message are required"
                })
                continue

            # Save message to database
            db = SessionLocal()
            try:
                db_message = ChatMessage(
                    resume_id=resume_id,
                    username=message_data["username"],
                    message=message_data["message"]
                )
                db.add(db_message)
                db.commit()
                db.refresh(db_message)

                # Broadcast to all connected clients
                response = {
                    "id": db_message.id,
                    "resume_id": db_message.resume_id,
                    "username": db_message.username,
                    "message": db_message.message,
                    "created_at": db_message.created_at.isoformat()
                }
                await manager.broadcast(response, resume_id)
            finally:
                db.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket, resume_id)

