import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGO_URL = str(os.getenv("MONGO_URL"))

mongo_client = MongoClient(MONGO_URL, server_api=ServerApi('1'))
