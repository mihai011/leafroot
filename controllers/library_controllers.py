"""Library Controllers"""

from fastapi import APIRouter


from controllers import create_response, CurrentUser, MongoDatabase
from data import Library, BookPackage

library_router = APIRouter(prefix="/library", tags=["library"])


@library_router.post("/book")
async def add_book(_: CurrentUser, mongo_db: MongoDatabase, book: BookPackage):
    """Controller add book to library"""
    await Library.AddItem(mongo_db, book)
    return create_response("Book added!", 200)


@library_router.get("/books")
async def get_books(_: CurrentUser, mongo_db: MongoDatabase):
    """Get all books from library"""
    response = await Library.GetItemsByFilter(mongo_db, {})
    return create_response("Books retrieved!", 200, item=response)


@library_router.delete("/book/{item_id}")
async def delete_books(_: CurrentUser, mongo_db: MongoDatabase, item_id: str):
    """Delete a book by id from library"""
    response = await Library.DeleteItemById(mongo_db, item_id)
    return create_response("Books retrieved!", 200, item=response)
