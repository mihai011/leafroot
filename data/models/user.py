"""
Used module related data
"""

import graphene
from jose import jwt

from sqlalchemy import Column, String
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

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


# classes necessary for graphql functionality,
# pretty useless for now, and I don't recommend them


class UserGraph(SQLAlchemyObjectType):
    """
    class for grtaphene to sqlalchemy
    """

    class Meta:
        """
        class meta
        """

        model = User


class UserFilter(FilterSet):
    """
    class for filtering user
    """

    class Meta:
        """
        meta class for user filtering
        """

        model = User
        fields = {"username": ["eq", "ne", "in", "ilike"]}

    @staticmethod
    def is_admin_filter(value):
        """
        method for fitlering admins
        """
        if value:
            return User.username == "admin"

        return User.username != "admin"


class QueryUser(graphene.ObjectType):
    """
    Query user for User class
    """

    list_users = graphene.List(UserGraph)
    get_user_id = graphene.Field(UserGraph, user_id=graphene.NonNull(graphene.Int))
    all_users = graphene.List(UserGraph, filters=UserFilter())

    def resolve_list_users(self, info):
        """
        method for resolving list of parameters
        """
        query = UserGraph.get_query(info)  # SQLAlchemy query

        query = query.filter
        return query.all()

    def resolve_get_user_id(self, user_id, session):
        """
        getting a user id
        """
        return User.GetById(user_id, session)
