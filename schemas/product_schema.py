# product_schema.py: This is your data validation and API contract layer
# These classes define what data your API accepts or returns. This is your "public face" to clients.

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    title: str
    manufacturer: str
    price: float
    description: str


class ProductResponse(ProductCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
