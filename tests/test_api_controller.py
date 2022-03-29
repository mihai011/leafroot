"""
Module for testing api controller
"""
import pytest

from tests import DataSource
from tests.conftest import temp_db


@pytest.mark.asyncio
@temp_db
async def test_api(session):
    """
    test api request controller
    """

    ds = DataSource(session)
    await ds.make_user()

    payload_api = {
        "name": "laguna",
        "method": "GET",
    }

    response = await ds.client.post("/api/external", json=payload_api, headers=ds.headers["Test_user"])
    assert response.status_code == 200
    assert response.status_code