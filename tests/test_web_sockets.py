"""Module for testing web sockets."""

import pytest

from tests import DataSource
from tests.conftest import temp_db


@pytest.mark.asyncio
@temp_db
async def test_web_sockets(session):
    """testing web sockets"""

    ds = DataSource(session)

    with ds.test_client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
