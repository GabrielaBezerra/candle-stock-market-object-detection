from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Bot:
    def __init__(self):
        # Path to the Chrome driver executable
        # download chrome and chrome driver at https://googlechromelabs.github.io/chrome-for-testing/
        if platform == "win32":
            self.driver_path = "drivers/win64/chromedriver.exe"
        elif platform == "linux":
            self.driver_path = "drivers/linux64/chromedriver"
        elif platform == "darwin":
            self.driver_path = "drivers/mac-arm64/chromedriver"
        self.service = Service(self.driver_path)
        # Start chrome saving cache and cookies
        options = Options()
        options.add_argument("--user-data-dir=chrome-data")
        self.driver = webdriver.Chrome(service=self.service, options=options)
        # Open the website
        self.driver.get("https://iqoption.com/traderoom")

    # TODO: Implement the buy and sell methods
    def buy(self):
        # Store iframe web element
        iframe = self.driver.find_element(By.CSS_SELECTOR, "#modal > iframe")
        # switch to selected iframe
        self.driver.switch_to.frame(iframe)
        pass

    def sell(self):
        pass

    def stop(self):
        self.driver.quit()
        self.service.stop()
