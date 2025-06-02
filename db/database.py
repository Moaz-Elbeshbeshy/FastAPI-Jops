import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from core.config import settings

logger = logging.getLogger(__name__)

# declare them as global placeholders, can be assigned later and accessed across different functions/modules.
client = None
db = None


async def connect_db():
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.DB_NAME]
        logger.info(f"✅ Connected to MongoDB database: {settings.DB_NAME}")
    except PyMongoError as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise e


async def close_db():
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")


async def get_db():
    return db
