# product_model.py: This is your internal data model
# These classes might be used internally, sometimes to help shape data from the DB (especially with MongoDB), or used with an ODM (like Beanie or Motor + custom logic).

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Product(BaseModel):
    title: str
    manufacturer: str
    price: float
    description: str
    user_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
