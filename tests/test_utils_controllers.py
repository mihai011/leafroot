"""Testing the health check."""

import json

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from tests import DataSource


async def test_health_status(async_session: AsyncSession) -> None:
    """Verifying the health check."""
    ds = DataSource(async_session)
    await ds.make_user()

    response = await ds.client.get(
        "/utils/health_check",
        headers=ds.headers["Test_user"],
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.text)
    health_check_ok = {
        "postgressql": True,
        "redis": True,
        "rabbitmq": True,
        "mongo": True,
        "spark": True,
        "kafka": True,
        "surrealdb": True,
        "scylladb": True,
        "cassandradb": True,
    }
    assert response_data["item"] == health_check_ok
