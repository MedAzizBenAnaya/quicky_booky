from pydantic import BaseModel, Field
from datetime import datetime


class Item(BaseModel):
    book_id: str
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    price: float = Field(..., ge=0, description="Price per item must be non-negative")


class Cart(BaseModel):
    cart_id: str
    user_id: str
    items: list
    created_at: datetime = Field(default_factory=datetime.utcnow())
    deleted_at: datetime
