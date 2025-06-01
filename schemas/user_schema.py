from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    user: User
    token: Token
