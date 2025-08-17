"""Configuration module for testing."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, drop_database

from app.app import app
from cache import initialize_cache
from config import config
from data import (
    Base,
    MyMinio,
    get_async_session,
    get_minio_client,
    get_mongo_client,
    get_mongo_database,
    get_object_storage_client,
    get_sync_session,
)
from logger import initialize_logger

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorClient

pytestmark = pytest.mark.asyncio


async def resolve_session(session_type: str) -> AsyncSession | Session:
    """Creating async and sync session for testing."""
    database_name = uuid4()
    db_url_base_sync = f"{config.sqlalchemy_database_url_base_sync}{database_name}"
    db_url_base_async = f"{config.sqlalchemy_database_url_base_async}{database_name}"
    engine_sync = create_engine(db_url_base_sync)

    create_database(db_url_base_sync)

    drop_database(db_url_base_sync)
    create_database(db_url_base_sync)
    # Create test database and tables
    Base.metadata.create_all(engine_sync)
    engine_async = create_async_engine(db_url_base_async)
    async_session_maker = sessionmaker(
        engine_async,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    sync_session_maker = sessionmaker(
        engine_sync,
        class_=Session,
        expire_on_commit=False,
    )

    async def override_async_session() -> AsyncSession:
        async with async_session_maker() as async_session:
            yield async_session
        await asyncio.shield(async_session.close())

    async def override_sync_session() -> Session:
        with sync_session_maker() as sync_session:
            yield sync_session
        sync_session.close()

    app.dependency_overrides[get_async_session] = override_async_session
    app.dependency_overrides[get_sync_session] = override_sync_session

    session = sync_session_maker()

    if session_type == "async":
        session = async_session_maker()
    yield session

    if session_type == "async":
        await asyncio.shield(session.close())
    else:
        session.close()

    app.dependency_overrides[get_async_session] = get_async_session
    app.dependency_overrides[get_sync_session] = get_sync_session
    drop_database(db_url_base_sync)
    yield 0


@pytest.fixture
async def async_session() -> AsyncSession:
    """Pytest fixture for SQLAlchemy postgresql session."""
    session_generator = resolve_session("async")
    session = await session_generator.__anext__()
    yield session
    await session_generator.__anext__()


@pytest.fixture
async def sync_session() -> Session:
    """Pytest fixture for SQLAlchemy postgresql session."""
    session_generator = resolve_session("sync")
    session = await session_generator.__anext__()
    yield session
    await session_generator.__anext__()


@pytest.fixture
async def mongo_db() -> AsyncIOMotorClient:
    """Mongodb fixture for mongodb MotorAsync client."""
    database_name = uuid4()
    mongo_client = await anext(get_mongo_client())  # noqa
    mongo_db = mongo_client[str(database_name)]

    async def override_mongo_db() -> AsyncIOMotorClient:
        yield mongo_db

    app.dependency_overrides[get_mongo_database] = override_mongo_db
    yield mongo_db
    await mongo_client.drop_database(str(database_name))
    mongo_client.close()
    app.dependency_overrides[get_mongo_database] = get_mongo_database


@pytest.fixture
async def minio_storage() -> AsyncIOMotorClient:
    """Minio fixture for miniopy_async client."""
    bucket_name = str(uuid4()).replace("-", "")
    minio_client = get_minio_client()
    minio_object = MyMinio(bucket_name, minio_client)
    await minio_object.make_bucket()

    async def override_minio_storage() -> AsyncIOMotorClient:
        yield minio_object

    app.dependency_overrides[get_object_storage_client] = override_minio_storage
    yield minio_object
    # Remove the test bucket
    await minio_object.remove_bucket()
    app.dependency_overrides[get_object_storage_client] = get_object_storage_client


@pytest.fixture(autouse=True)
def initiation_for_test() -> None:
    """This executes just before each test."""
    initialize_logger()
    initialize_cache()
