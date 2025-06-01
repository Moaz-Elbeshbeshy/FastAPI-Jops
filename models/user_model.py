from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, v):
        email_regex = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v


class UserInDB(User):
    hashed_password: str
