from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class Address(BaseModel):
    street: str
    house_number: str
    zip: int
    state: str
    country: str


class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    password: str
    phone: str

    created_books: list
    orders: list
    role: str
    address: Address
    created_at: datetime = Field(default_factory=datetime.utcnow())
    deleted_at: datetime
