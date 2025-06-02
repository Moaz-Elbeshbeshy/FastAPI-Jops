# register_user(user: UserCreateSchema)
# Purpose: Register a new user.

# Steps:

# Connects to the database.

# Checks if the email is already registered.

# Hashes the user's password.

# Stores the user (without the plain password) in MongoDB.

# Generates a JWT access token.

# Returns user data + the token.

# 🔑 login_user(login_data: LoginRequestSchema)
# Purpose: Log in a user.

# Steps:

# Connects to the database.

# Finds the user by email.

# Verifies the password.

# If correct, returns a new JWT access to


from fastapi import HTTPException, status
from schemas.user_schema import UserCreateSchema, UserResponseSchema
from schemas.auth_schema import LoginRequestSchema
from motor.motor_asyncio import AsyncIOMotorClient
from core.security import hash_password, create_access_token, verify_password
from db.database import get_db


async def register_user(user: UserCreateSchema) -> UserResponseSchema:
    db = await get_db()
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = hash_password(user.password)
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    result = await db.users.insert_one(
        user_dict
    )  # will create a users collection in the db and insert document in it.
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


async def login_user(login_data: LoginRequestSchema):
    db = await get_db()
    existing_user = await db.users.find_one({"email": login_data.email})

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(login_data.password, existing_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": existing_user["email"]})

    return {"access_token": access_token, "token_type": "bearer"}
