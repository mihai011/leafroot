from fastapi.testclient import TestClient

import asyncio

from app.app import app
from data.models import get_session 

client = TestClient(app)

def temp_db(f):
    async def func(SessionLocal, *args, **kwargs):
        #Sessionmaker instance to connect to test DB
        #  (SessionLocal)From fixture

        async def override_get_db():
            async with SessionLocal() as session:
              yield session
            await session.close()

        #get to use SessionLocal received from fixture_Force db change
        app.dependency_overrides[get_session] = override_get_db
        # Run tests
        await f(*args, **kwargs)
        # get_Undo db
        app.dependency_overrides[get_session] = get_session
    return func