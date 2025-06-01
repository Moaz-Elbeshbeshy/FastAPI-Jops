from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Job(BaseModel):
    title: str
    company: str
    location: str
    description: str
    user_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
