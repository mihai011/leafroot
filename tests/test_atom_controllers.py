"""
Module for testing particles
"""
import pytest
from httpx import AsyncClient

import nest_asyncio

from app.app import app
from data.models import temp_db
from tests import DataSource

nest_asyncio.apply()

@pytest.mark.asyncio
@temp_db
async def test_particles():
    """
    testing particles
    """

    ds = DataSource()

    # make proton
    payload = {"charge": 123.23}
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/atoms/proton", headers=ds.headers, json=payload)
        assert response.status_code == 200

        response = await client.get("/atoms/proton", params=payload, headers=ds.headers)
        assert response.status_code == 200
