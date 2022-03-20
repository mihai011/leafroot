"""
Used module related data
"""

from jose import jwt

from sqlalchemy import Column, String
from data.models import ExtraBase, Base
from data.models import secret

class User(Base, ExtraBase):
    """
    Class that resembles a user model
    """

    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_pass = Column(String(256), unique=True, nullable=False)
    permissions = Column(String(3))

    def __repr__(self):
        return "<User %r>" % self.username
