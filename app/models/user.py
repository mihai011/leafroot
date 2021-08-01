from sqlalchemy.sql.sqltypes import Boolean
from models import ExtraBase, Base

from sqlalchemy import Column, Integer, String


class User(Base, ExtraBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    verified = Column(Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username