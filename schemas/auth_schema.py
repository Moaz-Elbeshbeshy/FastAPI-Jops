from pydantic import BaseModel, EmailStr


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str
