"""Module for testing particles models."""
import pytest

from data import Neutron, Proton, Electron, Atom


@pytest.mark.asyncio
async def test_atom_model(async_session):
    """Simple test for Atom model."""

    atom_args = {"x": 1.0, "y": 1.0, "z": 1.0}
    atom_obj = await Atom.AddNew(async_session, atom_args)

    assert atom_obj.x == 1.0
    assert atom_obj.y == 1.0
    assert atom_obj.z == 1.0


@pytest.mark.asyncio
async def test_sub_atomic_model(async_session):
    """Test for subparticles of atom."""

    atom_args = {"x": 1.0, "y": 1.0, "z": 1.0}
    atom_obj = await Atom.AddNew(async_session, atom_args)

    neutron_args = {"charge": 1.0, "atom_id": atom_obj.id}
    await Neutron.AddNew(async_session, neutron_args)

    proton_args = {"charge": 1.0, "atom_id": atom_obj.id}
    await Proton.AddNew(async_session, proton_args)

    electron_args = {"charge": 1.0, "atom_id": atom_obj.id}
    await Electron.AddNew(async_session, electron_args)

    await async_session.refresh(atom_obj)
    atom_obj = await Atom.GetById(async_session, atom_obj.id)

    assert len(atom_obj.neutrons) == 1
    assert len(atom_obj.protons) == 1
    assert len(atom_obj.electrons) == 1
