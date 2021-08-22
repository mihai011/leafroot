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
SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}/{}"\
    .format("postgresql+asyncpg",os.getenv("POSTGRES_USER"),\
    os.getenv("POSTGRES_PASSWORD"), "db", os.getenv("POSTGRES_DB") )

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
session = SessionMaker()

Base = declarative_base()

secret = '$QmB*R>Nq!$.YdzkKvt{fBX7<Bmgm4~gy")&IthT+AtkA>/C@BkDyL0vRTraG"g'


class ExtraBase(SerializerMixin):

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime, default = datetime.now())


    def serialize(self):

        return self.to_dict()


    @classmethod
    def AddNew(Cls, args):

        obj = Cls(**args)
        session.add(obj)
        session.commit()

        return obj

    @classmethod
    def GetAll(Cls):

        return session.query(Cls).all()

    @classmethod
    def GetById(Cls, id):

        obj = session.query(Cls).where(Cls.id==id).first()
        if not obj:
            return None

        return obj.serialize()

    @classmethod
    async def GetByArgs(Cls, args):

        current_session = SessionMaker()

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
