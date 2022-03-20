"""
Module for testing particles controller
"""
import pytest

import nest_asyncio
from tests import DataSource
from tests.conftest import temp_db

nest_asyncio.apply()


@pytest.mark.asyncio
@temp_db
async def test_particles(session):
    """
    testing particles
    """

    ds = DataSource()
    await ds.make_user()
    # make proton
    payload_particle = {"charge": 123.23}
    payload_atom = {"x": 1, "y": 1, "z": 1}

    response = await ds.client.post(
        "/atoms/create_atom", headers=ds.headers["Test_user"], json=payload_atom
    )
    assert response.status_code == 200

    response = await ds.client.post(
        "/atoms/proton", headers=ds.headers["Test_user"], json=payload_particle
    )
    assert response.status_code == 200

    response = await ds.client.get(
        "/atoms/proton", params=payload_particle, headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200

    response = await ds.client.post(
        "/atoms/neutron", headers=ds.headers["Test_user"], json=payload_particle
    )
    assert response.status_code == 200

    response = await ds.client.get(
        "/atoms/neutron", params=payload_particle, headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200

    response = await ds.client.post(
        "/atoms/electron", headers=ds.headers["Test_user"], json=payload_particle
    )
    assert response.status_code == 200

    response = await ds.client.get(
        "/atoms/electron", params=payload_particle, headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200
