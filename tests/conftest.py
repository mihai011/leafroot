"""
Configuration module for testing
"""
import random
import string

import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database, create_database

from data import Base, get_session
from data import SQLALCHEMY_DATABASE_URL_BASE_SYNC, SQLALCHEMY_DATABASE_URL_BASE_ASYNC

from app.app import app


@pytest.fixture(scope="function")
def SessionLocalGenerator():
    """
    settings of test database
    """
    letters = string.ascii_lowercase
    name = "".join(random.choice(letters) for i in range(10))
    DB_URL_BASE_SYNC = "{}{}".format(SQLALCHEMY_DATABASE_URL_BASE_SYNC, name)
    DB_URL_BASE_ASYNC = "{}{}".format(SQLALCHEMY_DATABASE_URL_BASE_ASYNC, name)
    engine_sync = create_engine(DB_URL_BASE_SYNC)

    # assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL),
    # "Test database already exists. Aborting tests."
    try:
        create_database(DB_URL_BASE_SYNC)
    except Exception:
        drop_database(DB_URL_BASE_SYNC)
        create_database(DB_URL_BASE_SYNC)
    # Create test database and tables
    Base.metadata.create_all(engine_sync)
    engine_async = create_async_engine(DB_URL_BASE_ASYNC)
    given_session_maker = sessionmaker(
        engine_async, class_=AsyncSession, expire_on_commit=False
    )

    # Run the tests
    yield given_session_maker

    # Drop the test database
    drop_database(DB_URL_BASE_SYNC)


def temp_db(test_function):
    """
    pytest fixture to create a temp date
    """

    async def func(SessionLocalGenerator, *args, **kwargs):
        # Sessionmaker instance to connect to test DB
        # (SessionLocal) From fixture

        async def override_get_db():
            async with SessionLocalGenerator() as session:
                yield session
            await session.close()

        async def override_get_db_simple():
            async with SessionLocalGenerator() as session:
                return session

        kwargs['session'] = await override_get_db_simple()

        # get to use SessionLocalGenerator received from fixture_Force db change
        app.dependency_overrides[get_session] = override_get_db
        # Run tests
        await test_function(*args, **kwargs)
        # get_Undo db
        await kwargs['session'].close()
        app.dependency_overrides[get_session] = get_session

    return func
