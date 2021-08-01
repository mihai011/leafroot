import os
from datetime import datetime
import graphene

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from graphene_sqlalchemy import SQLAlchemyObjectType



load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}/{}"\
    .format("postgresql",os.getenv("POSTGRES_USER"),\
    os.getenv("POSTGRES_PASSWORD"), "db", os.getenv("POSTGRES_DB") )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

Base = declarative_base()

class ExtraBase:

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



from models.user import User

class UserGraph(SQLAlchemyObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    list_users = graphene.List(UserGraph)

    def resolve_hello(self, info, name):
        return "Hello " + name

    def resolve_list_users(self, info):
        return User.GetAll()


