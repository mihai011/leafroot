"""Testing db populate"""

from tests import DataSource


async def test_lot_users(async_session):
    """Add a lot of users in db"""

    NUMBER_OF_USERS = 100

    ds = DataSource(async_session)

    await ds.make_users(NUMBER_OF_USERS)

    return True
