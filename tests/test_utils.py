"""Tests for util functions."""

import pytest
from fastapi import HTTPException

from tests.conftest import temp_db
from utils import create_access_token, authenthicate_user
from data import User


@temp_db("both")
async def test_authenticate(async_session, sync_session):
    """test authenthication."""

    user_args = {
        "username": "test_name",
        "email": "test@gmail.com",
        "hashed_pass": "fake_pass",
    }

    user_orig = await User.AddNew(async_session, user_args)
    data = user_orig.serialize()
    data.pop("id")
    data.pop("created_at")
    data.pop("updated_at")
    token = create_access_token(data)
    user_auth = authenthicate_user(token, sync_session)

    assert user_orig.id == user_auth.id


@temp_db("sync_session")
async def test_fake_user(session):
    """Test authenthication with fake creds."""

    user_args = {
        "username": "test_name",
        "email": "test@gmail.com",
        "hashed_pass": "fake_pass",
    }
    token = create_access_token(user_args)

    with pytest.raises(HTTPException):
        authenthicate_user(token, session)
