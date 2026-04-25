from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models.user import User
from models.todo import Todo
from models.food import Food

async def init_mongo():
    client = AsyncIOMotorClient(
        "mongodb+srv://elizabet:password@cs-topicsi.biphwto.mongodb.net/?appName=cs-topicsi"
    )

    db = client["job_app_db"]

    print("✅ Connecting to MongoDB...")

    await init_beanie(
        database=db,
        document_models=[User, Food, Todo]
    )

    print("✅ MongoDB connected and Beanie initialized")

    return client