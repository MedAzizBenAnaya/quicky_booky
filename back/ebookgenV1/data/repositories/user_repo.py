import datetime
from typing import Optional, List
from bson import ObjectId
from back.ebookgenV1.data.db_connection import mongodb
from .book_repo import BookRepository  # Import BookRepository
from .order_repo import OrderRepository  # Import OrderRepository
from ..modules.users import User


class UserRepository:
    def __init__(self):
        self.collection = mongodb.db["users"]
        self.book_repo = BookRepository()  # Instantiate BookRepository
        self.order_repo = OrderRepository()  # Instantiate OrderRepository

    async def create_user(self, user_data: dict) -> str:
        user = User(**user_data)
        user_dict = user.dict()

        if "created_at" not in user_dict:
            user_dict["created_at"] = datetime.datetime.utcnow()

        user_dict["updated_at"] = user_dict.get("updated_at", None)

        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["user_id"] = str(user["_id"])  # Convert ObjectId to string
            user.pop("_id", None)
            # Fetch user's books and orders
            user["created_books"] = await self.get_user_books(user_id)
            user["orders"] = await self.get_user_orders(user_id)
        return user

    async def get_user_by_email(self, email: str) -> Optional[dict]:

        user = await self.collection.find_one({"email": email})
        if user:
            user["user_id"] = str(user["_id"])  # Convert ObjectId to string
            user.pop("_id", None)
            # Fetch user's books and orders
            user["created_books"] = await self.get_user_books(user["user_id"])
            user["orders"] = await self.get_user_orders(user["user_id"])
        return user

    async def update_user(self, user_id: str, update_data: dict) -> bool:
        update_data["updated_at"] = datetime.datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_user(self, user_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"deleted_at": datetime.datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def get_user_books(self, user_id: str) -> List[dict]:
        books = await self.book_repo.get_books_by_user(user_id)
        return books

    async def get_user_orders(self, user_id: str) -> List[dict]:
        orders = await self.order_repo.get_orders_by_user(user_id)
        return orders
