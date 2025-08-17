"""Testing db populate."""

from sqlalchemy.ext.asyncio import AsyncSession

from tests import DataSource


async def test_lot_users(async_session: AsyncSession) -> bool:
    """Add a lot of users in db."""
    number_of_users = 100

    ds = DataSource(async_session)

    await ds.make_users(number_of_users)

    return True
