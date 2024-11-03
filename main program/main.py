import json
from selenium import webdriver
from test_runner import TestRunner

if __name__ == "__main__":
    with open("scenario1.json", "r") as file:
        scenario = json.load(file)
    
    driver = webdriver.Chrome()
    test_runner = TestRunner(driver)
    test_runner.run_test(scenario)
