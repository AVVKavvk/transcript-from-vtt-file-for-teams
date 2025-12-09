from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from app.utils.logger import logger
import os


load_dotenv()


if os.getenv("MONGODB_URL") is None:
    raise Exception("MONGODB_URL is not set")

try:
    mongo_client = AsyncIOMotorClient(
        os.getenv("MONGODB_URL"), server_api=ServerApi("1")
    )
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")

db_name = os.getenv("DB_NAME")
