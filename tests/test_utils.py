"""Tests for util functions."""

import pytest
from fastapi import HTTPException

from utils import authenthicate_user, create_access_token


async def test_fake_user(async_session):
    """Test authenthication with fake creds."""

    user_args = {
        "username": "test_name",
        "email": "test@gmail.com",
        "hashed_pass": "fake_pass",
    }
    token = create_access_token(user_args)

    with pytest.raises(HTTPException):
        await authenthicate_user(token, async_session)
