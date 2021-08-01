import os
from datetime import datetime

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, Boolean, DateTime, String

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

class ExtraBase:

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime, default = datetime.now())


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

        return session.query(Cls).filter(Cls.id==id).first()

    @classmethod
    def GetByArgs(Cls, args):

        query = session.query(Cls)

        for attr,value in args.items():
            query = query.filter( getattr(Cls,attr) == value )

        return query.all()
        

# all models imported here

from models.user import QueryUser, User
