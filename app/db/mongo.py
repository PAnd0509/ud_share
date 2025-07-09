from pymongo import MongoClient
from app.config.settings import MONGO_URL

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["ud_sharem"]
