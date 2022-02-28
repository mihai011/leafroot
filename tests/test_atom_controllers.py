"""
Module for testing particles
"""
import pytest
from httpx import AsyncClient

import nest_asyncio
from app.app import app
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

    # make proton
    payload_particle = {"charge": 123.23}
    payload_atom = {"x": 1, "y": 1, "z": 1}
    async with AsyncClient(app=app, base_url="http://test") as client:

        response = await client.post(
            "/atoms/create_atom", headers=ds.headers, json=payload_atom
        )
        assert response.status_code == 200

        response = await client.post(
            "/atoms/proton", headers=ds.headers, json=payload_particle
        )
        assert response.status_code == 200

        response = await client.get(
            "/atoms/proton", params=payload_particle, headers=ds.headers
        )
        assert response.status_code == 200

        response = await client.post(
            "/atoms/neutron", headers=ds.headers, json=payload_particle
        )
        assert response.status_code == 200

        response = await client.get(
            "/atoms/neutron", params=payload_particle, headers=ds.headers
        )
        assert response.status_code == 200

        response = await client.post(
            "/atoms/electron", headers=ds.headers, json=payload_particle
        )
        assert response.status_code == 200

        response = await client.get(
            "/atoms/electron", params=payload_particle, headers=ds.headers
        )
        assert response.status_code == 200

