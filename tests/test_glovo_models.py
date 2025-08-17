"""Test Glovo Queries."""

import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from data import Curier, Order, OrderItem, Product, Restaurant, User


async def test_glovo_queries(async_session: AsyncSession) -> None:
    """Testing sqlalchemy queries."""
    total_users = 100
    users_that_order = 10
    total_restaurants = 10
    available_restaurants = 10
    total_products = 100
    total_curiers = 100
    available_curiers = 5

    users = [
        await User.add_new(
            async_session,
            {"username": str(i), "email": str(i), "hashed_pass": str(i)},
        )
        for i in range(total_users)
    ]

    users_that_make_orders = list(
        {secrets.choice(users) for _ in range(users_that_order)},
    )

    restaurants = [
        await Restaurant.add_new(async_session, {"name": str(i)})
        for i in range(total_restaurants)
    ]

    available_restaurants = list(
        {secrets.choice(restaurants) for _ in range(available_restaurants)},
    )

    products = [
        await Product.add_new(
            async_session,
            {
                "name": str(i),
                "restaurant_id": secrets.choice(available_restaurants).id,
            },
        )
        for i in range(total_products)
    ]
    ordered_products = list({secrets.choice(products) for _ in range(10)})

    curiers = [
        await Curier.add_new(async_session, {"name": str(i), "price": i})
        for i in range(total_curiers)
    ]

    active_curiers = list({secrets.choice(curiers) for _ in range(available_curiers)})
    orders = []

    for curier in active_curiers:
        for user in users_that_make_orders:
            o = await Order.add_new(
                async_session,
                {"curier_id": curier.id, "client_id": user.id},
            )
            orders.append(o)

    for order in orders:
        for product in ordered_products:
            await OrderItem.add_new(
                async_session,
                {
                    "product_id": product.id,
                    "order_id": order.id,
                },
            )

    user_id = secrets.choice(users_that_make_orders).id
    user_orders = await Order.get_orders_by_client_id(async_session, user_id)
    user_products = await Product.get_products_by_client_id(async_session, user_id)
    assert len(user_products) == len(user_orders) * len(ordered_products)
