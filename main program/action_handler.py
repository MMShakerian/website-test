from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from validator import Validator
from alert_handler import AlertHandler
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
                expected_error_selectors = action.get("expected_error_selector")
                expected_error = action.get("expected_error")
                
                print(f"Starting invalid values test for selector '{selector}'")
                
                # ابتدا مقادیر نامعتبر را تست کن
                Validator(self.driver).test_invalid_values(selector, action["rules"], expected_error_selectors, expected_error)
                
                # کلیک خالی انجام بده (می‌توانید این قسمت را با کلیک بر روی یک عنصر خالی در صفحه انجام دهید)
                self.driver.find_element("css selector", "body").click()
                
                # اسکرول به پایین صفحه برای دیدن عنصر
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # یک وقفه کوتاه برای اسکرول
                
                # افزایش زمان انتظار برای پیام خطا
                if isinstance(expected_error_selectors, list):
                    error_displayed = False
                    for error_selector in expected_error_selectors:
                        try:
                            WebDriverWait(self.driver, 30).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, error_selector))
                            )
                            print(f"Expected error message for selector '{error_selector}' is displayed.")
                            error_displayed = True
                            break
                        except:
                            print(f"Expected error message for selector '{error_selector}' is NOT displayed.")
                    
                    if not error_displayed:
                        print("No expected error messages were displayed.")
                else:
                    # اگر فقط یک مقدار باشد (رشته)
                    try:
                        WebDriverWait(self.driver, 30).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, expected_error_selectors))
                        )
                        print(f"Expected error message for selector '{expected_error_selectors}' is displayed.")
                    except:
                        print(f"Expected error message for selector '{expected_error_selectors}' is NOT displayed.")
                
                print(f"Completed invalid values test for selector '{selector}'")

            # سپس مقدار معتبر را وارد کن
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
