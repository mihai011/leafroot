"""
Atom class related models
"""

from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship


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
