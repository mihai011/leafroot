"""
Used module related data
"""


from sqlalchemy import Column, String
from data.models import ExtraBase, Base


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

    def serialize(self):

        serialization = super().serialize()

        to_pop = ["hashed_pass", "permissions"]

        for field in to_pop:
            serialization.pop(field)

        return serialization
