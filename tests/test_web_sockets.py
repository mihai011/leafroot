"""Module for testing web sockets."""

from sqlalchemy.ext.asyncio import AsyncSession

from tests import DataSource


async def test_web_sockets(async_session: AsyncSession) -> None:
    """Testing web sockets."""
    ds = DataSource(async_session)
    with ds.test_client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Connected!"
        websocket.send_text("Stop!")
        data = websocket.receive_text()
        assert data == "Closed!"
