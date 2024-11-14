from pymongo import MongoClient
import time

class Logger:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="logsDB4", collection_name="logs"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log(self, message):
        # چاپ در کنسول
        print(message)
        
        # ذخیره در MongoDB
        self.collection.insert_one({"message": message})

    def close(self):
        self.client.close()
