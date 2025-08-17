"""General util module."""

from __future__ import annotations

import hashlib
import secrets
import string
import uuid
from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from redis.asyncio import Redis

from cache import my_key_builder, testproof_cache
from config import config
from data import User
from logger import log

if TYPE_CHECKING:
    from redis.asyncio import Redis
    from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@log()
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a hashed password is identical to another hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


@log()
def get_password_hash(password: str) -> str:
    """Produce the hash of a password."""
    return pwd_context.hash(password)


@log()
def make_short_hash(string: str) -> int:
    """Short hash for a string."""
    return int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (10**8)  # noqa


@log()
async def store_string_at_key(redis_client: Redis, key: str, store_string: str) -> None:
    """Store string at key in redis."""
    await redis_client.set(key, store_string)


@log()
async def get_string_at_key(redis_client: Redis, key: str) -> str:
    """Store string at key in redis."""
    return await redis_client.get(key)


@log()
def create_access_token(
    data: dict,
) -> str:
    """Create the access token hash for data."""
    return jwt.encode(data, config.secret_key, algorithm=config.algorithm)


@log()
@testproof_cache(expire=config.access_token_expire_seconds, key_builder=my_key_builder)
async def authenthicate_user(token: str, session: Session) -> User:
    """Authenticate a token."""
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token!",
        ) from e

    users = await User.get_by_args(session, payload)

    if len(users) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user found!",
        )

    return users[0]


@log()
def random_string() -> str:
    """Make a random string."""
    init_pepper = "R"
    r_string = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10)
    )

    return init_pepper + r_string


@log()
def is_valid_uuid(val: str) -> bool | None:
    """Check if a val is a valid UUID."""
    try:
        uuid.UUID(str(val))
    except ValueError:
        return False
    return True
