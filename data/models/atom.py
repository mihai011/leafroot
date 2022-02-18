"""
Atom class related models
"""

from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy import select


from data.models import ExtraBase, Base


class Atom(Base, ExtraBase):
    """
    Atom class represents
    """

    __tablename__ = "atoms"

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    neutrons = relationship("Neutron")
    protons = relationship("Proton")
    electrons = relationship("Electron")

    @classmethod
    async def AddNew(cls, session, args):

        obj = await super().AddNew(session, args)

        result = await session.execute(
            select(cls)
            .filter(cls.id == obj.id)
            .options(
                selectinload(cls.neutrons),
                selectinload(cls.electrons),
                selectinload(cls.protons),
            )
        )
        obj = result.scalars().first()

        return obj


class Proton(Base, ExtraBase):
    """
    class that represents a proton
    """

    __tablename__ = "protons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey("atoms.id"))


class Neutron(Base, ExtraBase):
    """
    class that represents a neutron
    """

    __tablename__ = "neutrons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey("atoms.id"))


class Electron(Base, ExtraBase):
    """
    class that represents an electron
    """

    __tablename__ = "electrons"

    charge = Column(Float)
    atom_id = Column(Integer, ForeignKey("atoms.id"))
