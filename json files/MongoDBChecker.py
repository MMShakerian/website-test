import pymongo
from tkinter import messagebox

class MongoDBChecker:
    def __init__(self, db_name, collection_name , host="mongodb://localhost:27017/", port=27017):
        try:
            # اتصال به پایگاه داده MongoDB
            self.client = pymongo.MongoClient(host, port)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")

    def check_values(self, action_type, selector):
        """
        بررسی می‌کند که آیا ترکیب مقادیر `action_type` و `selector`
        به ترتیب در پایگاه داده با `tag_name` و `xpath` مطابقت دارد یا خیر.
        """
        try:
            # تبدیل مقدار selector به فرم مورد نظر
            formatted_selector = f'id("{selector}")'
            
            # آماده‌سازی پرس‌وجو برای پایگاه داده
            query = {
                "tag_name": action_type,
                "xpath": formatted_selector
            }
            
            # جستجو در پایگاه داده
            result = self.collection.find_one(query)
            
            if result:
                return True
            return False
        except Exception as e:
            messagebox.showerror("Database Error", f"Error querying the database: {e}")
            return False

