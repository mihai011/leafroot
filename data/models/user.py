import graphene
from jose import jwt

from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, Boolean, String
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import  FilterSet

from data.models import ExtraBase, Base, session
from data.models import secret


class Token(Base, ExtraBase):
    __tablename__ = "tokens"

    token = Column(String)

    @classmethod
    async def AddNew(Cls, session, args):

        token = jwt.encode(args, secret, algorithm='HS256')

        obj = Cls(token=token)
        session.add(obj)
        await session.commit()

        return obj

    @classmethod
    async def Search(Cls, session, args):

        token = jwt.encode(args, secret, algorithm='HS256')

        actual_token = await Cls.GetByArgs({'token':token}, session)

        if actual_token:
            return actual_token[0]
        else:
            return None
    

class User(Base, ExtraBase):
    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    permissions = Column(String(3))
        
    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    async def AddNew(Cls, session, args):

        user = Cls(**args)
        session.add(user)
        await session.commit()

        return user

        
# classes necessary for graphql functionality, 
# pretty useless for now, and I don't recommend them

class UserGraph(SQLAlchemyObjectType):
    class Meta:
        model = User

class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['eq', 'ne', 'in', 'ilike']
        }

    @staticmethod
    def is_admin_filter(info, query, value):
        if value:
            return User.username == 'admin'
        else:
            return User.username != 'admin'

class QueryUser(graphene.ObjectType):
    list_users = graphene.List(UserGraph)
    get_user_id = graphene.Field(UserGraph, user_id=graphene.NonNull(graphene.Int))
    all_users = graphene.List(UserGraph, filters=UserFilter())

    def resolve_list_users(self, info):
        query = UserGraph.get_query(info)  # SQLAlchemy query

        query = query.filter
        return query.all()

    def resolve_get_user_id(self, info, user_id):
        return User.GetById(user_id)