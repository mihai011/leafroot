"""
General util module
"""

from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from config import config
from data import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    """
    verifies if a hashed password is identical to another hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    """
    produces the hash of a password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[int] = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]),
):
    """
    creates the access token hash for data
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
    )
    return encoded_jwt


async def authenthicate_user(token, session):
    """
    Authenticates users given a token
    """
    try:
        payload = jwt.decode(
            token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]]
        )
    except Exception:
        return None

    users = await User.GetByArgs(session, {"email": payload["email"]})
    if not users:
        return None

    return users[0]
