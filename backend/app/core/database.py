# backend/app/core/database.py
"""
Database initialization and connection management
"""

import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Global engine and session factory
engine = None
async_session = None

async def init_database(timeout: int = 30):
    """Initialize database connection with timeout"""
    global engine, async_session

    if settings.DB_TYPE == "sqlite":
        # SQLite for development
        database_url = "sqlite+aiosqlite:///./skg_goat.db"
    else:
        # PostgreSQL for production
        database_url = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

    try:
        engine = create_async_engine(
            database_url,
            echo=settings.DEBUG,
            pool_pre_ping=True,
        )

        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        # Test connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: None)

        # Create tables
        from app.models.user import Base as UserBase
        from app.models.order import Base as OrderBase
        async with engine.begin() as conn:
            await conn.run_sync(UserBase.metadata.create_all)
            await conn.run_sync(OrderBase.metadata.create_all)

    except Exception as e:
        raise RuntimeError(f"Database initialization failed: {e}")

async def get_db() -> AsyncSession:
    """Get database session"""
    if async_session is None:
        raise RuntimeError("Database not initialized")
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_db_status() -> bool:
    """Check database connectivity"""
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text("SELECT 1")))
        return True
    except:
        return False