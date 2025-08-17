"""Module for photo objects."""

import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from data import Base, ExtraBase


class Photo(Base, ExtraBase):
    """Class that resembles a photo model."""

    __tablename__ = "photos"

    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User")
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    photo_name = Column(String(80), unique=False, nullable=False)

    def create_storage_path(self) -> str:
        """Create a bucket path."""
        return f"{self.user_id}/photos/{self.uuid}/{self.photo_name}"
