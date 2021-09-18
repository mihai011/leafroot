import os
from datetime import datetime
import json

from dotenv import load_dotenv
from sqlalchemy import pool

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, DateTime

from jose import jwt


load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL_ASYNC = "{}://{}:{}@{}/{}"\
    .format("postgresql+asyncpg",os.getenv("POSTGRES_USER"),\
    os.getenv("POSTGRES_PASSWORD"), "db", os.getenv("POSTGRES_DB") )

SQLALCHEMY_DATABASE_URL_SYNC = "{}://{}:{}@{}/{}"\
    .format("postgresql",os.getenv("POSTGRES_USER"),\
    os.getenv("POSTGRES_PASSWORD"), "db", os.getenv("POSTGRES_DB") )

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC, echo=False, future=True
)


Base = declarative_base()
secret = '$QmB*R>Nq!$.YdzkKvt{fBX7<Bmgm4~gy")&IthT+AtkA>/C@BkDyL0vRTraG"g'

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


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

        obj = await session.query(Cls).where(Cls.id==id).first()
        if not obj:
            return None

        return obj.serialize()

    @classmethod
    async def GetByArgs(Cls, session, args):

        current_session = session

        def filter_sync(session):
            query = session.query(Cls)
            for attr,value in args.items():
                query = query.filter( getattr(Cls,attr) == value )
            return query.all()

        results = await current_session.run_sync(filter_sync)

        await current_session.close()

        return results
        

# all models imported here

from models.user import QueryUser, User, Token
