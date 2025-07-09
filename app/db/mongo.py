from pymongo import MongoClient
from app.config.settings import MONGO_URL, MONGO_DB
from app.scripts.init_mongo import init_collections

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
init_collections(db)