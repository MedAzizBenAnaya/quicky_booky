import datetime
from typing import Optional, List
from bson import ObjectId
from back.ebookgenV1.data.db_connection import mongodb
from back.ebookgenV1.data.modules.books import Book
import gridfs


class BookRepository:
    def __init__(self):
        self.collection = mongodb.db["books"]
        self.fs = gridfs.AsyncGridFS(mongodb.db)

        
    async def create_book(self, book_data: dict) -> str:
        book = Book(**book_data)
        book_dict = book.dict()

        if "created_at" not in book_dict:
            book_dict["created_at"] = datetime.datetime.utcnow()

        book_dict["updated_at"] = book_dict.get("updated_at", None)

        result = await self.collection.insert_one(book_dict)
        return str(result.inserted_id)

    async def get_book_by_id(self, book_id: str) -> Optional[dict]:
        book = await self.collection.find_one({"_id": ObjectId(book_id)})
        if book:
            book["book_id"] = str(book["_id"])  # Convert ObjectId to string
            book.pop("_id", None)
        return book

    async def get_books_by_user(self, user_id: str) -> List[dict]:
        books = await self.collection.find({"user_id": user_id}).to_list(length=None)
        for book in books:
            book["book_id"] = str(book["_id"])
            book.pop("_id", None)
        return books

    async def update_book(self, book_id: str, update_data: dict) -> bool:
        update_data["updated_at"] = datetime.datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_book(self, book_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": {"deleted_at": datetime.datetime.utcnow()}}
        )
        return result.modified_count > 0
