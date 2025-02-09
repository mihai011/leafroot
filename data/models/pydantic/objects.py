"""Pydantic class for objects."""

from typing import Literal
from pydantic import BaseModel, StrictBytes


class PhotoPacket(BaseModel):
    """Photo Class Model."""

    photo_name: str
    photo_type: Literal["jpg", "png", "gif"]
    photo_body: StrictBytes

    class Config:
        """Config class."""

        example = {
            "photo_id": 1,
            "photo_name": "photo1.jpg",
            "photo_path": "/photos/photo1.jpg",
            "photo_type": "jpg",
            "photo_hash": "1234567890",
            "photo_body": "1234567890",
        }
