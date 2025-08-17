"""Pydantic models related to user."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr


class PydanticUser(BaseModel):
    """Pydantinc User class."""

    username: str | None
    email: str | None
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
    permissions: str | None

    class Config:
        """Pydantic config class for user."""

        example = {
            "username": "username",
            "email": "example@email.com",
            "password": "password",
        }
