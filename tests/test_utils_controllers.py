"""Testing the health check."""

import pytest
import json

from tests import DataSource
from tests.conftest import temp_db


@pytest.mark.asyncio
@temp_db
async def test_health_status(session):
    """Verifying the health check."""

    ds = DataSource(session)
    await ds.make_user()

    response = await ds.client.get(
        "/utils/health_check", headers=ds.headers["Test_user"]
    )

    assert response.status_code == 200
    response_data = json.loads(response.text)
    health_check_ok = {"postgressql": True, "redis": True, "rabbitmq": True}
    assert response_data["item"] == health_check_ok
