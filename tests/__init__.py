from fastapi.testclient import TestClient

import asyncio

from app.app import app
from data.models import get_session 

client = TestClient(app)
