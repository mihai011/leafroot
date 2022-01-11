import os
from datetime import datetime
import json
from typing import final

from jose import jwt
from sqlalchemy import pool
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, DateTime

from app import config

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL_ASYNC = "{}://{}:{}@{}/{}"\
    .format("postgresql+asyncpg",config["POSTGRES_USER"],\
    config["POSTGRES_PASSWORD"], "db", config["POSTGRES_DB"] )

SQLALCHEMY_DATABASE_URL_SYNC = "{}://{}:{}@{}/{}"\
    .format("postgresql", config["POSTGRES_USER"],\
    config["POSTGRES_PASSWORD"], "db", config["POSTGRES_DB"] )

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC, echo=False, future=True, pool_size=0,max_overflow=100,
    connect_args={'timeout':500}
)

async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
secret = '$QmB*R>Nq!$.YdzkKvt{fBX7<Bmgm4~gy")&IthT+AtkA>/C@BkDyL0vRTraG"g'


async def get_session() -> AsyncSession:
    
    async with async_session() as session:
        yield session

    await session.close()

async def get_session_simple() -> AsyncSession:

    async with async_session() as session:
        return session
    

class ExtraBase(SerializerMixin):

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime, default = datetime.now())

    def serialize(self):
        return self.to_dict()

    @classmethod
    async def AddNew(Cls, session, args):

        obj = Cls(**args)
        session.add(obj)
        await session.commit()

        return obj

    @classmethod
    async def GetAll(Cls, session):

        return await session.query(Cls).all()

    @classmethod
    async def GetById(Cls, id, session):

        query = select(Cls).where(Cls.id == id)
        result = await session.execute(query)
        (obj,) = result.one()
        if not obj:
            return None

        return obj.serialize()

    @classmethod
    async def GetByArgs(Cls, session, args):

        def filter_sync(session):
            query = session.query(Cls)
            for attr,value in args.items():
                query = query.filter( getattr(Cls,attr) == value )
            return query.all()

        results = await session.run_sync(filter_sync)

        await session.close()

        return results

    @classmethod
    async def DeleteAll(Cls, session):

        def delete(session):
            query = session.query(Cls).delete()

        await session.run_sync(delete)
        await session.commit()
        return True
