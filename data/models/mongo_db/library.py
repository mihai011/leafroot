"""Class for the mongo Library."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from data.models.mongo_db import BaseMongo


class Book(BaseModel):
    """Book class model for mongodb."""

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)

    class Config:
        """Config class."""

        validate_by_name = True
        json_json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "...",
            },
        }


class BookUpdate(BaseModel):
    """Book class model update for mongodb."""

    title: str | None
    author: str | None
    synopsis: str | None

    class Config:
        """Config class."""

        json_schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes...",
            },
        }


class Library(BaseMongo):
    """Library class."""

    collection__name = "library"


class BookPackage(BaseModel):
    """Book Package top be received by controllers."""

    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)

    class Config:
        """Config class."""

        json_schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "...",
            },
        }
