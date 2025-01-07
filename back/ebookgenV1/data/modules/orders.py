from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class OrderItems(BaseModel):
    book_id: str
    quantity: int


class Order(BaseModel):
    order_id: str
    items: list[str]
    user_id: str
    status: str
    created_at: Field(default_factory=datetime.utcnow())
    updated_at: Optional[datetime] | None
