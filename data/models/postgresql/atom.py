"""Atom class related models."""

from sqlalchemy import Column, Float, ForeignKey, Integer, select
from sqlalchemy.orm import relationship, selectinload

from data.models.postgresql import Base, ExtraBase


class Atom(Base, ExtraBase):
    """Atom class."""

    __tablename__ = "atoms"

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    neutrons = relationship("Neutron")
    protons = relationship("Proton")
    electrons = relationship("Electron")

    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    async def AddNew(cls, session, args):
        obj = await super().AddNew(session, args)
        obj = await cls.GetById(session, obj.id)

        return obj

    @classmethod
    async def GetById(cls, session, obj_id):
        result = await session.execute(
            select(cls)
            .options(
                selectinload(cls.neutrons),
                selectinload(cls.electrons),
                selectinload(cls.protons),
            )
            .filter(cls.id == obj_id)
        )
        obj = result.scalars().first()

        return obj


class Proton(Base, ExtraBase):
    """Class that represents a proton."""

    __tablename__ = "protons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey("atoms.id"))


class Neutron(Base, ExtraBase):
    """Class that represents a neutron."""

    __tablename__ = "neutrons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey("atoms.id"))


class Electron(Base, ExtraBase):
    """Class that represents an electron."""

    __tablename__ = "electrons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey("atoms.id"))
