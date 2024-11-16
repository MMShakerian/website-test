from pymongo import MongoClient
import time

class Logger:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="logsDB9", collection_name="logs"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log(self, message, selector=None):
        # چاپ در کنسول
        print(f"{message} | Selector: {selector}")

        
        # ذخیره در MongoDB
        log_entry = {
            "message": message
        }
       
        log_entry["selector"] = selector
        
        self.collection.insert_one(log_entry)

    def close(self):
        self.client.close()
