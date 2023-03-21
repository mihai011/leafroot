"""Module for testing web sockets."""

import pytest  # pylint: disable=R0801

from tests import DataSource  # pylint: disable=R0801
from tests.conftest import temp_db  # pylint: disable=R0801


@pytest.mark.asyncio
@temp_db("async_session")
async def test_web_sockets(session):
    """Testing web sockets."""

    ds = DataSource(session)
    with ds.test_client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Connected!"
        websocket.send_text("Stop!")
        data = websocket.receive_text()
        assert data == "Closed!"
