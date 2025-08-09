"""Testing the quote controllers."""

import json

from fastapi import status
import pytest

from tests import DataSource


async def test_quotes(async_session):
    """Verifying the quotes endpoint."""

    ds = DataSource(async_session)
    await ds.make_user()

    payload_quote = {"quote": "test", "author": "author"}

    response = await ds.client.post(
        "/quotes/quote", headers=ds.headers["Test_user"], json=payload_quote
    )
    assert response.status_code == status.HTTP_200_OK
    response = await ds.client.get(
        "/quotes/quote", headers=ds.headers["Test_user"]
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.text)
    assert response_data["item"]["quote"] == payload_quote["quote"]
