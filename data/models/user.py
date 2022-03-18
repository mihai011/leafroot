"""
Used module related data
"""

from jose import jwt

from sqlalchemy import Column, String
from data.models import ExtraBase, Base
from data.models import secret


class Token(Base, ExtraBase):
    """
    Token user by user for authenthication
    """

    __tablename__ = "tokens"

    token = Column(String)

    @classmethod
    async def AddNew(Cls, session, args):

        token = jwt.encode(args, secret, algorithm="HS256")

        obj = Cls(token=token)
        session.add(obj)
        await session.commit()

        return obj

    @classmethod
    async def Search(Cls, session, args):
        """
        Searching for token in db
        """

        token = jwt.encode(args, secret, algorithm="HS256")

        actual_token = await Cls.GetByArgs(session, {"token": token})

        if actual_token:
            return actual_token[0]

        return None


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
