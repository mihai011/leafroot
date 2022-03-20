"""
Module for testing particles models
"""
import pytest
import nest_asyncio

from tests.conftest import temp_db
from data import Neutron, Proton, Electron, Atom

nest_asyncio.apply()


@pytest.mark.asyncio
@temp_db
async def test_atom_model(session):

    atom_args = {"x": 1.0, "y": 1.0, "z": 1.0}
    atom_obj = await Atom.AddNew(session, atom_args)

    assert atom_obj.x == 1.0
    assert atom_obj.y == 1.0
    assert atom_obj.z == 1.0


@pytest.mark.asyncio
@temp_db
async def test_sub_atomic_model(session):

    atom_args = {"x": 1.0, "y": 1.0, "z": 1.0}
    atom_obj = await Atom.AddNew(session, atom_args)

    neutron_args = {"charge": 1.0, "atom_id": atom_obj.id}
    await Neutron.AddNew(session, neutron_args)

    proton_args = {"charge": 1.0, "atom_id": atom_obj.id}
    await Proton.AddNew(session, proton_args)

    electron_args = {"charge": 1.0, "atom_id": atom_obj.id}
    await Electron.AddNew(session, electron_args)

    await session.refresh(atom_obj)
    atom_obj = await Atom.GetById(session, atom_obj.id)

    assert len(atom_obj.neutrons) == 1
    assert len(atom_obj.protons) == 1
    assert len(atom_obj.electrons) == 1

    await session.close()
