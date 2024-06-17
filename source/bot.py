import time

from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Bot:
    def __init__(self):
        # download chrome e chrome driver: https://googlechromelabs.github.io/chrome-for-testing/
        if platform == "win32":
            self.driver_path = ".\\drivers\\win64\\chromedriver.exe"
        elif platform == "linux":
            self.driver_path = "drivers/linux64/chromedriver"
        elif platform == "darwin":
            self.driver_path = "drivers/mac-arm64/chromedriver"
        self.service = Service()
        options = Options()
        # opções de salvar cache e cookies
        # options.add_argument("--user-data-dir=chrome-data")
        self.driver = webdriver.Chrome(service=self.service, options=options)
        # abrir o site, logar e ir para a sala de negociação
        self.login()

    def login(self):
        self.driver.get("https://login.iqoption.com/pt/login")

        time.sleep(2)
        conatainer_email_element = self.driver.find_element(
            By.XPATH, '//div[@data-test-id="login-email-input"]'
        )
        input_email_element = conatainer_email_element.find_element(
            By.TAG_NAME, "input"
        )
        input_email_element.send_keys("gabriela.hotdog@hotmail.com")

        conatainer_password_element = self.driver.find_element(
            By.XPATH, '//div[@data-test-id="login-password-input"]'
        )
        input_password_element = conatainer_password_element.find_element(
            By.TAG_NAME, "input"
        )
        input_password_element.send_keys("pdi123")

        self.driver.find_element(
            By.XPATH, '//button[@data-test-id="login-submit-button"]'
        ).click()

        time.sleep(5)
        self.driver.get("https://iqoption.com/traderoom")

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
