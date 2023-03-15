"""General util module."""


import random
import string

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


from config import config
from cache import testproof_cache, my_key_builder
from logger import log


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
@testproof_cache(
    expire=int(config.access_token_expire_seconds), key_builder=my_key_builder
)
def create_access_token(
    data: dict,
):
    """Create the access token hash for data."""

    encoded_jwt = jwt.encode(
        data, config.secret_key, algorithm=config.algorithm
    )
    return encoded_jwt


@log()
@testproof_cache(
    expire=config.access_token_expire_seconds, key_builder=my_key_builder
)
def authenthicate_user(token: str):
    """Authenticate a token."""

    payload = jwt.decode(
        token, config.secret_key, algorithms=[config.algorithm]
    )

    return payload


@log()
def random_string():
    """Make a random string."""
    init_pepper = "R"
    r_string = "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(100)
    )

    return init_pepper + r_string
