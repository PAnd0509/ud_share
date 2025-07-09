
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
MONGO_URL    = os.getenv("MONGO_URL")
MONGO_DB     = os.getenv("MONGO_DB")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")