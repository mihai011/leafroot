"""Used module related data."""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

from data.models.postgresql import ExtraBase, Base


class User(Base, ExtraBase):
    """Class that resembles a user model."""

    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_pass = Column(String(256), unique=True, nullable=False)
    permissions = Column(String(3))
    address = Column(String(200))

    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    async def GetById(cls, session, obj_id):
        """Get object by his id."""

        query = select(cls).where(cls.id == obj_id)
        result = await session.execute(query)
        o = result.scalars().first()
        return o

    def serialize(self):
        serialization = super().serialize()

        to_pop = ["hashed_pass", "permissions"]

        for field in to_pop:
            serialization.pop(field)

        return serialization


class UserFollowRelation(Base, ExtraBase):
    """Class that resembles a user photo share model."""

    __tablename__ = "user_follow_relations"

    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    follower = relationship("User", foreign_keys=[follower_id])
    followed_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed = relationship("User", foreign_keys=[followed_id])
