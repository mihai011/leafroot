"""Tests for util functions."""

from tests.conftest import temp_db
from utils import create_access_token, authenthicate_user
from data import User


@temp_db
async def test_authenticate(session):
    """test authenthication."""

    user_args = {
        "username": "test_name",
        "email": "test@gmail.com",
        "hashed_pass": "fake_pass",
    }

    user_orig = await User.AddNew(session, user_args)
    token = create_access_token(user_orig.serialize())
    user_auth = authenthicate_user(token)

    assert user_orig.serialize() == user_auth


@temp_db
async def test_fake_user(session):
    """test authenthication with fake creds."""

    user_args = {
        "username": "test_name",
        "email": "test@gmail.com",
        "hashed_pass": "fake_pass",
    }
    token = create_access_token(user_args)
    user_auth = authenthicate_user(token)

    assert user_auth == user_args
