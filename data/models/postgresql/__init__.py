"""Models init file."""
from datetime import datetime

import asyncio
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, DateTime

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

async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
sync_session = sessionmaker(
    sync_engine, class_=Session, expire_on_commit=False
)

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
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def serialize(self):
        """Base serializer method."""
        return self.to_dict()

    @classmethod
    async def AddNew(cls, session, args):
        """Add object method."""

        obj = cls(**args)
        session.add(obj)
        await session.commit()

        return obj

    @classmethod
    async def GetAll(cls, session):
        """Get all objects method."""

        def get_all(session):
            return session.query(cls).all()

        return await session.run_sync(get_all)

    @classmethod
    async def GetById(cls, session, obj_id):
        """Get object by his id."""

        query = select(cls).where(cls.id == obj_id)
        result = await session.execute(query)
        object = result.scalars().first()
        return object

    @classmethod
    async def GetByArgs(cls, session, args):
        """Get object by args."""

        def filter_sync(session):
            query = session.query(cls)
            for attr, value in args.items():
                query = query.filter(getattr(cls, attr) == value)
            return query.all()

        if not args:
            return []

        results = await session.run_sync(filter_sync)

        await session.close()

        return results

    @classmethod
    def GetByArgsSync(cls, session, args):
        """Get object by args in a sync way."""

        query = session.query(cls)
        for attr, value in args.items():
            query = query.filter(getattr(cls, attr) == value)
        return query.all()

    @classmethod
    async def DeleteAll(Cls, session):
        """Delete all objects method."""

        def delete(session):
            session.query(Cls).delete()

        await session.run_sync(delete)
        await session.commit()
        return True

    @classmethod
    async def GetRandom(Cls, session):
        """Get random object."""

        def get_random(session):
            return session.query(Cls).order_by(func.random()).first()

        return await session.run_sync(get_random)
