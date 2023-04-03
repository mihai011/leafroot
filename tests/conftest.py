"""Configuration module for testing."""
from uuid import uuid4

import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import drop_database, create_database
import motor.motor_asyncio

from app.app import app
from data import Base, get_async_session, get_sync_session, get_mongo_client
from config import config


@pytest.fixture
def DatabasesObjects() -> None:
    """Set of test database."""
    database_name = uuid4()
    DB_URL_BASE_SYNC = "{}{}".format(
        config.sqlalchemy_database_url_base_sync, database_name
    )
    DB_URL_BASE_ASYNC = "{}{}".format(
        config.sqlalchemy_database_url_base_async, database_name
    )
    engine_sync = create_engine(DB_URL_BASE_SYNC)

    try:
        create_database(DB_URL_BASE_SYNC)
    except Exception:
        drop_database(DB_URL_BASE_SYNC)
        create_database(DB_URL_BASE_SYNC)
    # Create test database and tables
    Base.metadata.create_all(engine_sync)
    engine_async = create_async_engine(DB_URL_BASE_ASYNC)
    given_async_session_maker = sessionmaker(
        engine_async, class_=AsyncSession, expire_on_commit=False
    )
    given_sync_session_maker = sessionmaker(
        engine_sync, class_=Session, expire_on_commit=False
    )

    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
        config.mongo_url_auth
    )
    mongo_test_db = mongo_client[str(database_name)]

    # Run the tests
    yield (given_async_session_maker, given_sync_session_maker, mongo_test_db)

    # Drop the test database
    drop_database(DB_URL_BASE_SYNC)
    mongo_client.drop_database(str(database_name))


def temp_db(*test_args, **test_kwargs):
    """Pytest decorator to create a temp date."""

    def inner(test_function):
        async def func(DatabasesObjects, *args, **kwargs):
            # Sessionmaker instance to connect to test DB
            # (SessionLocalGenerator) From fixture

            async def override_async_session():
                async_generator = DatabasesObjects[0]
                async with async_generator() as async_session:
                    yield async_session
                await async_session.close()

            async def override_return_async_session():
                async_generator = DatabasesObjects[0]
                async with async_generator() as async_session:
                    return async_session

            def override_sync_session():
                sync_generator = DatabasesObjects[1]
                with sync_generator() as sync_session:
                    yield sync_session
                sync_session.close()

            def override_return_sync_session():
                sync_generator = DatabasesObjects[1]
                with sync_generator() as sync_session:
                    return sync_session

            def override_return_mongo_client():
                return DatabasesObjects[2]

            def override_mongo_client():
                yield DatabasesObjects[2]

            if "async_session" in test_args:
                kwargs["session"] = await override_return_async_session()
            if "sync_session" in test_args:
                kwargs["session"] = override_return_sync_session()
            if "mongo_db" in test_args:
                kwargs["mongo_db"] = override_return_mongo_client()
            if "both" in test_args:
                kwargs["async_session"] = await override_return_async_session()
                kwargs["sync_session"] = override_return_sync_session()

            # get to use SessionLocalGenerator received from fixture_Force db
            app.dependency_overrides[
                get_async_session
            ] = override_async_session
            app.dependency_overrides[get_sync_session] = override_sync_session
            app.dependency_overrides[get_mongo_client] = override_mongo_client
            # Run tests
            try:
                await test_function(*args, **kwargs)
            finally:
                # get_Undo db
                if "async_session" in test_args:
                    await kwargs["session"].close()
                if "sync_session" in test_args:
                    kwargs["session"].close()
                if "both" in test_args:
                    await kwargs["async_session"].close()
                    kwargs["sync_session"].close()

                app.dependency_overrides[get_async_session] = get_async_session
                app.dependency_overrides[get_sync_session] = get_sync_session
                app.dependency_overrides[get_mongo_client] = get_mongo_client

        return func

    return inner
