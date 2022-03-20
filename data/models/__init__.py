"""
models init file
"""

from datetime import datetime

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, DateTime

from app import config


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL_ASYNC = "{}://{}:{}@{}/{}".format(
    "postgresql+asyncpg",
    config["POSTGRES_USER"],
    config["POSTGRES_PASSWORD"],
    "db",
    config["POSTGRES_DB"],
)

SQLALCHEMY_DATABASE_URL_SYNC = "{}://{}:{}@{}/{}".format(
    "postgresql",
    config["POSTGRES_USER"],
    config["POSTGRES_PASSWORD"],
    "db",
    config["POSTGRES_DB"],
)

SQLALCHEMY_DATABASE_URL_BASE_SYNC = "{}://{}:{}@{}/".format(
    "postgresql", config["POSTGRES_USER"], config["POSTGRES_PASSWORD"], "db"
)

SQLALCHEMY_DATABASE_URL_BASE_ASYNC = "{}://{}:{}@{}/".format(
    "postgresql+asyncpg", config["POSTGRES_USER"], config["POSTGRES_PASSWORD"], "db"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC,
    echo=False,
    future=True,
    pool_size=0,
    max_overflow=100,
    connect_args={"timeout": 500},
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
secret = '$QmB*R>Nq!$.YdzkKvt{fBX7<Bmgm4~gy")&IthT+AtkA>/C@BkDyL0vRTraG"g'


async def get_session() -> AsyncSession:  # pragma: no cover
    """
    Yields an async session
    """

    async with async_session() as session:
        yield session

    await session.close()


class ExtraBase(SerializerMixin):
    """
    Extra base class used for child models
    """

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def serialize(self):
        """
        base serializer method
        """
        return self.to_dict()

    @classmethod
    async def AddNew(cls, session, args):
        """
        add object method
        """

        obj = cls(**args)
        session.add(obj)
        await session.commit()

        return obj

    @classmethod
    async def GetAll(cls, session):
        """
        Get all objects method
        """

        def get_all(session):
            return session.query(cls).all()

        return await session.run_sync(get_all)

    @classmethod
    async def GetById(cls, session, obj_id):
        """
        get object by his id
        """

        query = select(cls).where(cls.id == obj_id)
        result = await session.execute(query)
        objects = result.scalars().all()
        if not objects:
            return None

        return objects[0]

    @classmethod
    async def GetByArgs(cls, session, args):
        """
        get obejct by args
        """

        def filter_sync(session):
            query = session.query(cls)
            for attr, value in args.items():
                query = query.filter(getattr(cls, attr) == value)
            return query.all()

        results = await session.run_sync(filter_sync)

        await session.close()

        return results

    @classmethod
    async def DeleteAll(Cls, session):
        """
        Delete all objects method
        """

        def delete(session):
            session.query(Cls).delete()

        await session.run_sync(delete)
        await session.commit()
        return True
