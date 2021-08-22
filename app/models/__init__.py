import os
from datetime import datetime
import json

from dotenv import load_dotenv

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, DateTime

from jose import jwt


load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}/{}"\
    .format("postgresql",os.getenv("POSTGRES_USER"),\
    os.getenv("POSTGRES_PASSWORD"), "db", os.getenv("POSTGRES_DB") )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = session.query_property()

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

        obj = session.query(Cls).filter(Cls.id==id).first()
        if not obj:
            return None

        return obj.serialize()

    @classmethod
    def GetByArgs(Cls, args):

        query = session.query(Cls)

        for attr,value in args.items():
            query = query.filter( getattr(Cls,attr) == value )

        return query.all()
        

# all models imported here

from models.user import QueryUser, User, Token
