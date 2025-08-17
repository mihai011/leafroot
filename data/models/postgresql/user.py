"""Used module related data."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from data.models.postgresql import Base, ExtraBase


class User(Base, ExtraBase):
    """Class that resembles a user model."""

    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_pass = Column(String(256), unique=True, nullable=False)
    permissions = Column(String(3))
    address = Column(String(200))

    def __repr__(self) -> str:
        """Represenntation method."""
        return f"<User {self.username}>"

    @classmethod
    async def get_by_id(cls, session: AsyncSession, obj_id: int) -> "User":
        """Get object by his id."""
        query = select(cls).where(cls.id == obj_id)
        result = await session.execute(query)
        return result.scalars().first()

    def serialize(self) -> dict:
        """Method for object serialization."""
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
