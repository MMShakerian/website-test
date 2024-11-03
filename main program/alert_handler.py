from selenium.common.exceptions import NoAlertPresentException

class AlertHandler:
    def __init__(self, driver):
        self.driver = driver

    def handle_alert(self, selector):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(f"Handled alert with message: {alert_text} for field with selector '{selector}'")
        except NoAlertPresentException:
            pass
