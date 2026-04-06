from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.mongodb_url)
db = client[settings.mongodb_db]


def get_ips_collection():
    collection = db["ips"]
    collection.create_index("ip", unique=True)
    return collection