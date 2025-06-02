from fastapi import APIRouter, Depends
from controller.auth_controller import register_user, login_user
from schemas.auth_schema import LoginRequestSchema
from schemas.user_schema import UserCreateSchema, UserResponseSchema
from middleware.auth_middleware import get_current_user
from models.user_model import User


router = APIRouter()


@router.post("/register", response_model=UserResponseSchema)
async def register(user: UserCreateSchema):
    return await register_user(user)


@router.post("/login")
async def login(login_data: LoginRequestSchema):
    return await login_user(login_data)


@router.get("/me", response_model=UserResponseSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
