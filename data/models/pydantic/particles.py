"""Pydantic class for particle types."""

from typing import Optional

from pydantic import BaseModel


class PydanticAtom(BaseModel):
    """Atom Class Model."""

    x: float
    y: float
    z: float

    class Config:
        """Config class."""

        example = {"x": 1.23, "y": 3.2, "z": 4.5}


class PydanticElectron(BaseModel):
    """Electron Class Model."""

    charge: float
    atom_id: Optional[int]


class PydanticNeutron(BaseModel):
    """Neutron Class Model."""

    charge: float
    atom_id: Optional[int]


class PydanticProton(BaseModel):
    """Proton Class Model."""

    charge: float
    atom_id: Optional[int]
