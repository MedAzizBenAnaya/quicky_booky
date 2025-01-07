from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Book(BaseModel):
    book_id: str
    description: str
    user_id: str
    title: str
    category: str
    file_url: str
    file_format: str
    file_size_mb: float
    published_date: Optional[datetime] | None
    created_at: Field(default_factory=datetime.utcnow())
    updated_at: Optional[datetime] | None
