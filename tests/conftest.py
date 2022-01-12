import random
import string 

import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy import create_engine
from data import Base
from data.models import SQLALCHEMY_DATABASE_URL_ASYNC, SQLALCHEMY_DATABASE_URL_SYNC,\
    SQLALCHEMY_DATABASE_URL_BASE_SYNC, SQLALCHEMY_DATABASE_URL_BASE_ASYNC

@pytest.fixture(scope="function")
def SessionLocal():
    # settings of test database
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(10))
    DB_URL_BASE_SYNC = "{}{}".format(SQLALCHEMY_DATABASE_URL_BASE_SYNC ,name) 
    DB_URL_BASE_ASYNC = "{}{}".format(SQLALCHEMY_DATABASE_URL_BASE_ASYNC ,name) 
    engine_sync = create_engine(DB_URL_BASE_SYNC)

    # assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."
    try:
        create_database(DB_URL_BASE_SYNC)
    except:
        drop_database(DB_URL_BASE_SYNC)
        create_database(DB_URL_BASE_SYNC)
    # Create test database and tables
    Base.metadata.create_all(engine_sync)
    engine_async = create_async_engine(DB_URL_BASE_ASYNC)
    SessionLocal = sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)

    # Run the tests
    yield SessionLocal
    
    # Drop the test database
    drop_database(DB_URL_BASE_SYNC)

