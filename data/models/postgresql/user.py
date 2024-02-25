"""Used module related data."""


from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, selectinload
from data.models.postgresql import ExtraBase, Base


class User(Base, ExtraBase):
    """Class that resembles a user model."""

    __tablename__ = "users"

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_pass = Column(String(256), unique=True, nullable=False)
    permissions = Column(String(3))
    address = Column(String(200))
    photos = relationship("Photo", back_populates="user", lazy="select")

    def __repr__(self):
        return "<User %r>" % self.username

    @classmethod
    async def GetByArgs(cls, session, args):
        """Get object by args."""

        def filter_sync(session):
            query = session.query(cls)
            for attr, value in args.items():
                query = query.filter(getattr(cls, attr) == value)
                query = query.options(selectinload(cls.photos))
            return query.all()

        if not args:
            return []

        results = await session.run_sync(filter_sync)

        return results

    def serialize(self):
        serialization = super().serialize()

        to_pop = ["hashed_pass", "permissions"]

        for field in to_pop:
            serialization.pop(field)

        return serialization
