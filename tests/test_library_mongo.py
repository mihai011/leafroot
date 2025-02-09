"""Tests for mongo library models."""

import json
import pytest
from fastapi import status

from data import Library, Book, BookPackage
from tests import DataSource


@pytest.mark.asyncio
async def test_library(mongo_db):
    """Testing the mongodb class."""
    book1 = Book(title="test", author="test", synopsis="test")
    book2 = Book(title="test2", author="test2", synopsis="test2")
    assert await Library.AddItem(mongo_db, book1)
    assert await Library.AddItem(mongo_db, book2)

    books = await Library.GetItemsByFilter(mongo_db, {})
    assert len(books) == 2

    book_by_id = await Library.GetItemById(mongo_db, books[0]["id"])
    assert book_by_id["id"] == books[0]["id"]

    deleted = await Library.DeleteItemById(mongo_db, book_by_id["id"])
    assert deleted == 1

    books = await Library.GetItemsByFilter(mongo_db, {})
    assert len(books) == 1


@pytest.mark.asyncio
async def test_library_controllers(async_session, mongo_db):
    """Testing the library controllers."""

    ds = DataSource(async_session)
    await ds.make_user()

    book = BookPackage(title="test", author="test", synopsis="control")
    response = await ds.client.post(
        "/library/book",
        headers=ds.headers["Test_user"],
        data=book.model_dump_json(),
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        "/library/books",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.content)
    book_id = response_json["item"][0]["id"]

    response = await ds.client.delete(
        f"/library/book/{book_id}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.content)

    response = await ds.client.get(
        "/library/books",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.content)
    assert response_json["item"] == []
