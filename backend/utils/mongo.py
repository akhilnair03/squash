import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

# Fetch environment variables
db_password = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://akulshre:{db_password}@squash.a3sqp.mongodb.net/?retryWrites=true&w=majority&appName=Squash"