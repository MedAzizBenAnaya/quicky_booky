import datetime
from typing import Optional, List
from bson import ObjectId
from back.ebookgenV1.data.db_connection import mongodb
from back.ebookgenV1.data.models.orders import Order


class OrderRepository:
    def __init__(self):
        self.collection = mongodb.db["orders"]

    async def create_order(self, order_data: dict) -> str:
        order = Order(**order_data)
        order_dict = order.dict()

        if "created_at" not in order_dict:
            order_dict["created_at"] = datetime.datetime.utcnow()

        order_dict["updated_at"] = order_dict.get("updated_at", None)

        result = await self.collection.insert_one(order_dict)
        return str(result.inserted_id)

    async def get_order_by_id(self, order_id: str) -> Optional[dict]:
        order = await self.collection.find_one({"_id": ObjectId(order_id)})
        if order:
            order["order_id"] = str(order["_id"])
            order.pop("_id", None)
        return order

    async def get_orders_by_user(self, user_id: str) -> List[dict]:
        orders = await self.collection.find({"user_id": user_id}).to_list(length=None)
        for order in orders:
            order["order_id"] = str(order["_id"])
            order.pop("_id", None)
        return orders

    async def update_order(self, order_id: str, update_data: dict) -> bool:
        update_data["updated_at"] = datetime.datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_order(self, order_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"deleted_at": datetime.datetime.utcnow()}}
        )
        return result.modified_count > 0
