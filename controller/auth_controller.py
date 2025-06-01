from fastapi import HTTPException, status
from schemas.user_schema import UserCreate, UserResponse
from schemas.auth_schema import LoginRequest
from models.user_model import User
from core.security import hash_password, verify_password, create_access_token
from db.database import get_db
from bson import ObjectId


async def register_user(user: UserCreate) -> UserResponse:
    db = await get_db()
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)

    access_token = create_access_token({"sub": user_dict["email"]})

    return {
        "user": {
            "id": user_dict["id"],
            "name": user_dict["name"],
            "email": user_dict["email"],
        },
        "token": {"access_token": access_token, "token_type": "bearer"},
    }


async def login_user(login_data: LoginRequest):
    db = await get_db()
    user = await db.users.find_one({"email": login_data.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user["email"]})

    return {"access_token": access_token, "token_type": "bearer"}
