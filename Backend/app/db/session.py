from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool.impl import NullPool
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()


class DatabaseSessionManager:
    """Database session manager for handling connections"""
    
    def __init__(self):
        self._engine = None
        self._sessionmaker = None

    def init(self, host: str):
        """Initialize the database connection"""
        self._engine = create_async_engine(
            host,
            echo=settings.DEBUG,
            future=True,
            poolclass=NullPool,
            pool_pre_ping=True,
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def close(self):
        """Close database connections"""
        if self._engine is None:
            return
            
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncSession, None]:
        """Connect to database"""
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global session manager instance
sessionmanager = DatabaseSessionManager()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session"""
    async with sessionmanager.session() as session:
        yield session