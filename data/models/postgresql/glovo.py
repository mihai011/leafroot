"""Glovo models."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from data.models.postgresql import Base, ExtraBase


class Restaurant(Base, ExtraBase):
    """Restaurant class."""

    __tablename__ = "restaurants"

    name = Column(String)

    @classmethod
    async def get_restaurants_by_client_id(
        cls, session: AsyncSession, client_id: int
    ) -> None:
        """Get restaurants from which a user orders."""


class Product(Base, ExtraBase):
    """Product class."""

    __tablename__ = "products"

    name = Column(String)
    price = Column(Float)
    restaurant_id: Mapped[Integer] = mapped_column(ForeignKey("restaurants.id"))

    @classmethod
    async def get_products_by_client_id(
        cls, session: AsyncSession, client_id: int
    ) -> list:
        """Get all products ordered by a client."""
        join_query = (
            select(cls).join(OrderItem).join(Order).filter(Order.client_id == client_id)
        )

        result = await session.scalars(join_query)
        return result.all()


class Curier(Base, ExtraBase):
    """Curier Class."""

    __tablename__ = "curiers"

    name = Column(String)
    price = Column(Float)


class OrderItem(Base, ExtraBase):
    """Order Item."""

    __tablename__ = "orderitems"

    product_id: Mapped[Integer] = mapped_column(ForeignKey("products.id"))
    order_id: Mapped[Integer] = mapped_column(ForeignKey("orders.id"))
    quantity = Column(Integer)


class Order(Base, ExtraBase):
    """Order class."""

    __tablename__ = "orders"

    curier_id: Mapped[Integer] = mapped_column(ForeignKey("curiers.id"))
    client_id: Mapped[Integer] = mapped_column(ForeignKey("users.id"))

    @classmethod
    async def get_orders_by_client_id(
        cls, session: AsyncSession, client_id: int
    ) -> list:
        """Get all orders that belong to a client."""
        query = select(cls).where(cls.client_id == client_id)
        result = await session.scalars(query)
        return result.all()

    @classmethod
    async def get_orders_by_curier_id(
        cls, session: AsyncSession, curier_id: int
    ) -> list:
        """Get all orders that belong to a client."""
        query = select(cls).filter(cls.curier_id == curier_id)
        result = await session.scalars(query)
        return result.all()
