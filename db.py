from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://user:pass@cs-topicsi.biphwto.mongodb.net/"

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["fridge_app"]

users_collection = db["users"]
fridge_collection = db["fridge_items"]

