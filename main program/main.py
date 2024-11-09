import json
import os
from selenium import webdriver
from test_runner import TestRunner

# مسیر فولدر حاوی فایل‌های JSON را مشخص کنید
json_folder = "C:/Users/mohmmad moein/Desktop/python projects/website test/json files"

if __name__ == "__main__":
    # گرفتن لیست فایل‌های JSON در فولدر
    json_files = [file for file in os.listdir(json_folder) if file.endswith(".json")]
    
    driver = webdriver.Chrome()
    test_runner = TestRunner(driver)
    
    # اجرای تست برای هر فایل JSON
    for json_file in json_files:
        file_path = os.path.join(json_folder, json_file)
        with open(file_path, "r") as file:
            scenario = json.load(file)
        test_runner.run_test(scenario)
    
    driver.quit()
