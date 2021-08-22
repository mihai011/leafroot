import graphene

from sqlalchemy.sql.sqltypes import Boolean
from graphene import Connection, Node
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from models import ExtraBase, Base


class User(Base, ExtraBase):
    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    verified = Column(Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username



# classes necessary for graphql functionality

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