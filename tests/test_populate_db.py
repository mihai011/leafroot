"""Testing db populate"""

import pytest

from tests import DataSource


@pytest.mark.asyncio
async def test_lot_users(async_session):
    """Add a lot of users in db"""

    NUMBER_OF_USERS = 1000

    ds = DataSource(async_session)

    await ds.make_users(NUMBER_OF_USERS)

    users = await User.GetAll(async_session)
