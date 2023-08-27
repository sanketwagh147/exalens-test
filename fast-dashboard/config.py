import redis
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Final

mongo_uri:Final[str]  = "mongodb://mongodb:27017/"
client = AsyncIOMotorClient(mongo_uri)
db = client["sensor_data"]
readings_collection = db["readings"]

redis = redis.Redis(host="redis", port=6379, decode_responses=True)