from fastapi import APIRouter, Depends, HTTPException, status
from controller.auth_controller import register_user, login_user
from schemas.user_schema import UserCreate, UserResponse
from schemas.auth_schema import LoginRequest
from middleware.auth_middleware import get_current_user
from models.user_model import User

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await register_user(user)


@router.post("/login")
async def login(login_data: LoginRequest):
    return await login_user(login_data)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
