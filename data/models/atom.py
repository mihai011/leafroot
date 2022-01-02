import graphene
from jose import jwt

from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, Boolean, String, Float
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import  FilterSet

from data.models import ExtraBase, Base


class Atom(Base, ExtraBase):
  __tablename__ = "atoms"

  x = Column(Float)
  y = Column(Float)
  z = Column(Float)