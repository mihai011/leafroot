"""Atom class related models."""

from sqlalchemy import Column, Float, ForeignKey, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
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
    async def add_new(cls, session: AsyncSession, args: list) -> "Atom":
        """Adding an atom to the database."""
        obj = await super().add_new(session, args)
        return await cls.get_by_id(session, obj.id)

    @classmethod
    async def get_by_id(cls, session: AsyncSession, obj_id: int) -> "Atom":
        """Get the atom by id."""
        result = await session.execute(
            select(cls)
            .options(
                selectinload(cls.neutrons),
                selectinload(cls.electrons),
                selectinload(cls.protons),
            )
            .filter(cls.id == obj_id),
        )
        return result.scalars().first()


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
