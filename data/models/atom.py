from email.mime import base
import graphene
from jose import jwt

from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, Boolean, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from data.models import ExtraBase, Base


class Atom(Base, ExtraBase):
    __tablename__ = "atoms"

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    neutrons = relationship('Neutron')
    protons = relationship('Proton')
    electrons = relationship('Electron')


class Proton(Base, ExtraBase):
    __tablename__ = "protons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey('atoms.id'))


class Neutron(Base, ExtraBase):
    __tablename__ = "neutrons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey('atoms.id'))


class Electron(Base, ExtraBase):
    __tablename__ = "electrons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey('atoms.id'))
