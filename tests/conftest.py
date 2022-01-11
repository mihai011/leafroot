import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy import create_engine
from data import Base
from data.models import SQLALCHEMY_DATABASE_URL_ASYNC, SQLALCHEMY_DATABASE_URL_SYNC

@pytest.fixture(scope="function")
def SessionLocal():
    # settings of test database
    engine_sync = create_engine(SQLALCHEMY_DATABASE_URL_SYNC)

    # assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."
    try:
        create_database(SQLALCHEMY_DATABASE_URL_SYNC)
    except:
        drop_database(SQLALCHEMY_DATABASE_URL_SYNC)
        create_database(SQLALCHEMY_DATABASE_URL_SYNC)
    # Create test database and tables
    Base.metadata.create_all(engine_sync)
    engine_async = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)
    SessionLocal = sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)

    # Run the tests
    yield SessionLocal

    # Drop the test database
    drop_database(SQLALCHEMY_DATABASE_URL_SYNC)