"""Test Key Value controllers."""

from fastapi import status
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests import DataSource


async def test_keyvalue_controller(
    async_session: AsyncSession, mongo_db: AsyncIOMotorClient
) -> None:
    """Test key_value store."""
    ds = DataSource(async_session)
    await ds.make_user()

    response = await ds.client.post(
        "/keyvalue",
        headers=ds.headers["Test_user"],
        json={"key": "key", "value": "value"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Key Value added!"
    assert response.json()["item"] is None

    response = await ds.client.get("/keyvalue/key", headers=ds.headers["Test_user"])

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["item"] == "value"

    response = await ds.client.delete("/keyvalue/key", headers=ds.headers["Test_user"])

    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get("/keyvalue/key", headers=ds.headers["Test_user"])
    assert response.status_code == status.HTTP_404_NOT_FOUND
