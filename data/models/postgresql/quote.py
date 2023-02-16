"""Quote model."""

from sqlalchemy import Column, String
from data.models.postgresql import ExtraBase, Base


class Quote(Base, ExtraBase):
    """Quote class."""

    __tablename__ = "quotes"

    quote = Column(String)
    author = Column(String)
