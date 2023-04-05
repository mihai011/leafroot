"""Tests for mongo library models."""
import pytest
import json

from data import Library, Book, BookPackage
from tests.conftest import temp_db
from tests import DataSource


@pytest.mark.asyncio
@temp_db("mongo_db")
async def test_library(mongo_db):
    """Testing the mongodb class."""
    book1 = Book(title="test", author="test", synopsis="test")
    book2 = Book(title="test2", author="test2", synopsis="test2")
    assert await Library.AddItem(mongo_db, book1)
    assert await Library.AddItem(mongo_db, book2)

    books = await Library.GetAllBooks(mongo_db)
    assert len(books) == 2

    book_by_id = await Library.GetItemById(mongo_db, books[0]["id"])
    assert book_by_id["id"] == books[0]["id"]


@pytest.mark.asyncio
@temp_db("async_session", "mongo_db")
async def test_library_controllers(session, mongo_db):
    """Testing the library controllers"""

    ds = DataSource(session)
    await ds.make_user()

    book = BookPackage(title="test", author="test", synopsis="control")
    response = await ds.client.post(
        f"/library/book", headers=ds.headers["Test_user"], data=book.json()
    )
    assert response.status_code == 200
    status = json.loads(response.content)["status"]
    assert status == 200
