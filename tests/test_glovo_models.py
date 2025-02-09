"""Test Glovo Queries."""

import random

import pytest

from data import User, Curier, Restaurant, Order, Product, OrderItem


@pytest.mark.asyncio
async def test_glovo_queries(async_session):
    """Testing sqlalchemy queries."""

    TOTAL_USERS = 100
    USERS_THAT_ORDER = 10
    TOTAL_RESTAURANTS = 10
    AVAILABLE_RESTAURANTS = 10
    TOTAL_PRODUCTS = 100
    TOTAL_CURIERS = 100
    AVAILABLE_CURIERS = 5

    users = [
        await User.AddNew(
            async_session,
            {"username": str(i), "email": str(i), "hashed_pass": str(i)},
        )
        for i in range(TOTAL_USERS)
    ]

    users_that_make_orders = list(
        set(random.choice(users) for _ in range(USERS_THAT_ORDER))
    )

    restaurants = [
        await Restaurant.AddNew(async_session, {"name": str(i)})
        for i in range(TOTAL_RESTAURANTS)
    ]

    available_restaurants = list(
        set(random.choice(restaurants) for _ in range(AVAILABLE_RESTAURANTS))
    )

    products = [
        await Product.AddNew(
            async_session,
            {
                "name": str(i),
                "restaurant_id": random.choice(available_restaurants).id,
            },
        )
        for i in range(TOTAL_PRODUCTS)
    ]
    ordered_products = list(set(random.choice(products) for _ in range(10)))

    curiers = [
        await Curier.AddNew(async_session, {"name": str(i), "price": i})
        for i in range(TOTAL_CURIERS)
    ]

    active_curiers = list(
        set(random.choice(curiers) for _ in range(AVAILABLE_CURIERS))
    )
    orders = []

    for curier in active_curiers:
        for user in users_that_make_orders:
            o = await Order.AddNew(
                async_session,
                {"curier_id": curier.id, "client_id": user.id},
            )
            orders.append(o)

    for order in orders:
        for product in ordered_products:
            await OrderItem.AddNew(
                async_session,
                {
                    "product_id": product.id,
                    "order_id": order.id,
                },
            )

    user_id = random.choice(users_that_make_orders).id
    user_orders = await Order.getOrdersByClientId(async_session, user_id)
    user_products = await Product.getProductsbyClientId(async_session, user_id)
    assert len(user_products) == len(user_orders) * len(ordered_products)
