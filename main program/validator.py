from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from alert_handler import AlertHandler
import time

class Validator:
    def __init__(self, driver):
        self.driver = driver

    def test_invalid_values(self, selector, rules, expected_error_selector=None, expected_error=None):
        invalid_values = self.generate_invalid_values(rules)
        for invalid_value in invalid_values:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                element.clear()
                element.send_keys(invalid_value)
                time.sleep(1)
                
                print(f"Testing invalid value '{invalid_value}' for field with selector '{selector}'")
                
                self.driver.find_element(By.TAG_NAME, "body").click()
                time.sleep(0.5)
                
                if expected_error_selector:
                    self.check_error_message(selector, expected_error_selector, expected_error)
                else:
                    self.check_alert_or_value(selector, invalid_value, expected_error)
                
            except UnexpectedAlertPresentException:
                AlertHandler(self.driver).handle_alert(selector)
            except Exception as e:
                print(f"Error testing invalid value '{invalid_value}' for selector {selector}: {e}")

    def check_error_message(self, selector, error_selector, expected_error):
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, error_selector)
            error_text = error_element.text
            print(f"Error message shown for selector '{selector}': {error_text}")
            
            if expected_error and expected_error in error_text:
                print(f"Field with selector '{selector}' correctly displayed expected error: '{expected_error}'")
            else:
                print(f"Error message for selector '{selector}' did not match expected error.")
        
        except Exception:
            print(f"Error message element with selector '{error_selector}' not found for field '{selector}'.")

    def check_alert_or_value(self, selector, invalid_value, expected_error):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(f"Alert shown with message: {alert_text}")
            
            if expected_error and expected_error in alert_text:
                print(f"Field with selector '{selector}' correctly displayed expected error: '{expected_error}'")
            else:
                print(f"Error message for selector '{selector}' did not match expected error.")
        
        except NoAlertPresentException:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            if element.get_attribute("value") == invalid_value:
                print(f"Warning: Field with selector '{selector}' accepted invalid value '{invalid_value}'")
            else:
                print(f"Field with selector '{selector}' correctly rejected invalid value '{invalid_value}'")

    def generate_invalid_values(self, rules):
        invalid_values = []
        
        if "max_length" in rules:
            invalid_values.append("a" * (rules["max_length"] + 1))
        
        if "contains_digits" in rules and not rules["contains_digits"]:
            invalid_values.append("1234")
        
        if "allowed_characters" in rules:
            if rules["allowed_characters"] == "^[a-zA-Z]+$":
                invalid_values.append("!@#$%^&*()")
        
        return invalid_values
