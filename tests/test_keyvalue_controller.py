"""Test Key Value controllers."""

import pytest

from tests import DataSource


@pytest.mark.asyncio
async def test_keyvalue_controller(async_session, mongo_db):
    """Test key_value store"""
    ds = DataSource(async_session)
    await ds.make_user()

    response = await ds.client.post(
        "/keyvalue",
        headers=ds.headers["Test_user"],
        json={"key": "key", "value": "value"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Key Value added!"
    assert response.json()["item"] is None

    response = await ds.client.get(
        "/keyvalue/key", headers=ds.headers["Test_user"]
    )

    assert response.status_code == 200
    assert response.json()["item"] == "value"

    response = await ds.client.delete(
        "/keyvalue/key", headers=ds.headers["Test_user"]
    )

    assert response.status_code == 200

    response = await ds.client.get(
        "/keyvalue/key", headers=ds.headers["Test_user"]
    )
    assert response.status_code == 404
