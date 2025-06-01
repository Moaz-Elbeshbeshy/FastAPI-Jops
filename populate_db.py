import asyncio
from datetime import datetime, UTC
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
from core.security import hash_password


async def populate_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    # Clear existing collections
    await db.users.drop()
    await db.jobs.drop()

    # Insert sample users
    users = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "hashed_password": hash_password("password123"),
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "hashed_password": hash_password("password456"),
        },
    ]
    user_result = await db.users.insert_many(users)
    user_ids = [str(uid) for uid in user_result.inserted_ids]

    # Insert sample jobs
    jobs = [
        {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "location": "New York",
            "description": "Develop web applications",
            "user_id": user_ids[0],
            "created_at": datetime.now(UTC),
            "updated_at": None,
        },
        {
            "title": "Data Analyst",
            "company": "Data Inc",
            "location": "San Francisco",
            "description": "Analyze business data",
            "user_id": user_ids[1],
            "created_at": datetime.now(UTC),
            "updated_at": None,
        },
    ]
    await db.jobs.insert_many(jobs)

    print("Database populated with sample data")
    client.close()


if __name__ == "__main__":
    asyncio.run(populate_db())
