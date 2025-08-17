"""Library Controllers."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import CurrentUser, MongoDatabase, create_response
from data import BaseResponse, BookListResponseItem, BookPackage, Library

library_router = APIRouter(prefix="/library", tags=["library"])


@library_router.post("/book", response_model=BaseResponse)
async def add_book(
    _: CurrentUser,
    mongo_db: MongoDatabase,
    book: BookPackage,
) -> ORJSONResponse:
    """Controller add book to library."""
    awk = await Library.add_item(mongo_db, book)
    return create_response(
        message="Book added!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=awk,
    )


@library_router.get("/books", response_model=BookListResponseItem)
async def get_books(_: CurrentUser, mongo_db: MongoDatabase) -> ORJSONResponse:
    """Get all books from library."""
    response = await Library.get_items_by_filter(mongo_db, {})
    return create_response(
        message="Books retrieved!",
        status=status.HTTP_200_OK,
        response_model=BookListResponseItem,
        item=response,
    )


@library_router.delete("/book/{item_id}", response_model=BaseResponse)
async def delete_books(
    _: CurrentUser, mongo_db: MongoDatabase, item_id: str
) -> ORJSONResponse:
    """Delete a book by id from library."""
    response = await Library.delete_item_by_id(mongo_db, item_id)
    return create_response(
        message="Books deleted!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=response,
    )
