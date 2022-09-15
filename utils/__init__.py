"""General util module."""

from datetime import datetime, timedelta
from typing import Optional
import random
import string
import logging

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from config import config
from data import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a hashed password is identical to another hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """Produce the hash of a password."""
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[int] = int(config.access_token_expire_minutes),
):
    """Create the access token hash for data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.secret_key, algorithm=config.algorithm
    )
    logging.info("Created acces token for data: {}".format(data))
    return encoded_jwt


async def authenthicate_user(token: str, session):
    """Authenticate users given a token."""
    try:
        payload = jwt.decode(
            token, config.secret_key, algorithms=[config.algorithm]
        )
    except Exception as e:
        logging.error("Error on user authenthication")
        return None

    users = await User.GetByArgs(session, {"email": payload["email"]})
    if not users:
        logging.critical("User not found on authenthication")
        return None

    user = users[0]

    logging.info("User with name: {} authenthicated".format(user.username))

    return user


def random_string():
    """Make a random string."""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )
