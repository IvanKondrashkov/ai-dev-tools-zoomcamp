from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database import Session as SessionModel
from typing import Optional, Dict
import uuid


async def create_session(db: AsyncSession) -> str:
    """Create a new session and return session_id"""
    session_id = str(uuid.uuid4())
    session = SessionModel(
        session_id=session_id,
        code="// Write your code here\n",
        language="javascript",
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session_id


async def get_session(db: AsyncSession, session_id: str) -> Optional[Dict]:
    """Get session by session_id"""
    result = await db.execute(
        select(SessionModel).where(SessionModel.session_id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        return None
    return {
        "session_id": session.session_id,
        "code": session.code,
        "language": session.language,
    }


async def update_session_code(db: AsyncSession, session_id: str, code: str) -> bool:
    """Update session code"""
    result = await db.execute(
        update(SessionModel)
        .where(SessionModel.session_id == session_id)
        .values(code=code)
    )
    await db.commit()
    return result.rowcount > 0


async def update_session_language(db: AsyncSession, session_id: str, language: str) -> bool:
    """Update session language"""
    result = await db.execute(
        update(SessionModel)
        .where(SessionModel.session_id == session_id)
        .values(language=language)
    )
    await db.commit()
    return result.rowcount > 0


async def get_or_create_session(db: AsyncSession, session_id: str) -> Dict:
    """Get session or create if not exists"""
    session = await get_session(db, session_id)
    if session:
        return session
    
    # Create new session with the provided session_id
    session_obj = SessionModel(
        session_id=session_id,
        code="// Write your code here\n",
        language="javascript",
    )
    db.add(session_obj)
    await db.commit()
    await db.refresh(session_obj)
    
    return {
        "session_id": session_obj.session_id,
        "code": session_obj.code,
        "language": session_obj.language,
    }

