"""Models init file."""

import asyncio
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy_serializer import SerializerMixin

from cache import my_key_builder, testproof_cache
from config import config

async_engine = create_async_engine(
    config.sqlalchemy_database_url_async,
    echo=False,
    future=True,
    pool_size=0,
    max_overflow=100,
    connect_args={"timeout": 500},
    pool_pre_ping=True,
)

sync_engine = create_engine(
    config.sqlalchemy_database_url_sync,
    echo=False,
    future=True,
    pool_size=0,
    max_overflow=100,
    pool_pre_ping=True,
)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
sync_session = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)

Base = declarative_base()
secret = config.secret


async def get_async_session() -> AsyncSession:  # pragma: no cover
    """Yields an async session."""
    try:
        async with async_session() as session:
            yield session
    finally:
        await asyncio.shield(session.close())


async def get_sync_session() -> Session:  # pragma: no cover
    """Yields an sync session."""
    try:
        with sync_session() as session:
            yield session
    finally:
        session.close()


class ExtraBase(SerializerMixin):
    """Extra base class used for child models."""

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    def serialize(self) -> dict:
        """Base serializer method."""
        return self.to_dict()

    @classmethod
    async def add_new(cls, session: AsyncSession, args: list) -> "ExtraBase":
        """Add object method."""
        obj = cls(**args)
        session.add(obj)
        await session.commit()

        return obj

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list:
        """Get all objects method."""

        def get_all_sync(session: Session) -> list:
            return session.query(cls).all()

        return await session.run_sync(get_all_sync)

    @classmethod
    async def get_by_id(cls, session: AsyncSession, obj_id: int) -> "ExtraBase":
        """Get object by his id."""
        query = select(cls).where(cls.id == obj_id)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    @testproof_cache(key_builder=my_key_builder)
    async def get_by_args(cls, session: AsyncSession, args: list) -> "ExtraBase":
        """Get object by args."""

        def filter_sync(session: Session) -> list:
            query = session.query(cls)
            for attr, value in args.items():
                query = query.filter(getattr(cls, attr) == value)
            return query.all()

        if not args:
            return []

        return await session.run_sync(filter_sync)

    @classmethod
    def get_by_args_sync(cls, session: Session, args: list) -> list:
        """Get object by args in a sync way."""
        query = session.query(cls)
        for attr, value in args.items():
            query = query.filter(getattr(cls, attr) == value)
        return query.all()

    @classmethod
    async def delete_all(cls, session: AsyncSession) -> bool:
        """Delete all objects method."""

        def delete(session: Session) -> None:
            session.query(cls).delete()

        await session.run_sync(delete)
        await session.commit()
        return True

    @classmethod
    async def get_random(cls, session: AsyncSession) -> "ExtraBase":
        """Get random object."""

        def get_random_sync(session: Session) -> "ExtraBase":
            return session.query(cls).order_by(func.random()).first()

        return await session.run_sync(get_random_sync)
