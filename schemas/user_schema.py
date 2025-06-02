from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
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


class UserResponseSchema(BaseModel):
    user: User
    token: Token
