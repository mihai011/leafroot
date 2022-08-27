"""
tests for util functions
"""

from tests import DataSource
from tests.conftest import temp_db


@temp_db
async def test_small_task(session):
    """
    test authenthication
    """

    ds = DataSource(session)
    await ds.make_user()

    response = await ds.client.post(
        "/tasks/create_task", headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200
