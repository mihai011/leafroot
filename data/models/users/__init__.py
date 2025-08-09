"""Pydantic models related to user."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class PydanticUser(BaseModel):
    """Pydantinc User class."""

    username: Optional[str]
    email: Optional[str]
    password: str

    class Config:
        """Pydantic config class for user."""

        example = {
            "username": "username",
            "email": "example@email.com",
            "password": "password",
        }


class PydanticUserSignUp(BaseModel):
    """Pydantic class."""

    username: str
    email: EmailStr
    password: str
    permissions: Optional[str]

    class Config:
        """Pydantic config class for user."""

        example = {
            "username": "username",
            "email": "example@email.com",
            "password": "password",
        }
