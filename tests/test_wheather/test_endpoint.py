"""Tests for wheather data."""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from tests import DataSource

# from data import WheaterPoint # noqa


async def a_test_endopoint(async_session: AsyncSession) -> None:
    """Test endpoint for adding data."""
    ds = DataSource(async_session)
    await ds.make_user()

    data_point = ds.make_wheather_point()

    response = await ds.client.post(
        "/wheather",
        headers=ds.headers["Test_user"],
        json=data_point,
    )
    assert response.status_code == status.HTTP_200_OK
