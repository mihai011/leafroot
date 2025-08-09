"""Module for testing web sockets."""

from tests import DataSource  # pylint: disable=R0801


async def test_web_sockets(async_session):
    """Testing web sockets."""

    ds = DataSource(async_session)
    with ds.test_client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Connected!"
        websocket.send_text("Stop!")
        data = websocket.receive_text()
        assert data == "Closed!"
