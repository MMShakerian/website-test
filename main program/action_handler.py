from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from validator import Validator
from alert_handler import AlertHandler
import time

class ActionHandler:
    def __init__(self, driver):
        self.driver = driver

    def perform_action(self, action):
        selector = action["selector"]
        
        if action["action"] == "input":
            self.handle_input_action(action)
        elif action["action"] == "click":
            self.handle_click_action(selector)
    
    def handle_input_action(self, action):
        selector = action["selector"]
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            print(f"Found element for selector '{selector}'")
            
            if "rules" in action:
                expected_error_selector = action.get("expected_error_selector")
                expected_error = action.get("expected_error")
                print(f"Starting invalid values test for selector '{selector}'")
                
                Validator(self.driver).test_invalid_values(selector, action["rules"], expected_error_selector, expected_error)
                print(f"Completed invalid values test for selector '{selector}'")
            
            element.clear()
            print(f"Cleared field for selector '{selector}'")
            
            element.send_keys(action["value"])
            print(f"Entered '{action['value']}' in field with selector '{selector}'")
            time.sleep(1)
        
        except UnexpectedAlertPresentException:
            AlertHandler(self.driver).handle_alert(selector)
        except Exception as e:
            print(f"Error in input action for selector {selector}: {e}")

    def handle_click_action(self, selector):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            print(f"Found element for click action with selector '{selector}'")
            element.click()
            print(f"Clicked on element with selector '{selector}'")
        except UnexpectedAlertPresentException:
            AlertHandler(self.driver).handle_alert(selector)
        except Exception as e:
            print(f"Error in click action for selector {selector}: {e}")
