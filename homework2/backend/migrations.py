"""
Database migration script.
This script can be run to ensure database schema is up to date.
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from database import Base, DATABASE_URL


async def run_migrations():
    """Run database migrations"""
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"❌ Database migration failed: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_migrations())

