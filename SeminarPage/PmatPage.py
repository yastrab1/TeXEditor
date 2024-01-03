from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Config.Config import Config
from SeminarPage.AbstractSeminarPage import AbstractSeminarPage


class PmatPage(AbstractSeminarPage):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def authenticate(self):
        self.driver.get("https://pikomat.sk/")
        loginButton = self.driver.find_element(By.CSS_SELECTOR, "#app > nav > ul > button")
        loginButton.click()

        username = Config().get("P-matUsername")
        password = Config().get("P-matPassword")
        print(password)

        usernameInput = self.driver.find_element(By.ID, "formulate---1")
        passwordInput = self.driver.find_element(By.ID, "formulate---2")

        usernameInput.send_keys(username)
        passwordInput.send_keys(password)
        passwordInput.send_keys(Keys.RETURN)

        self.cookies = self.driver.get_cookies()
        print(self.cookies)

    def getPageHTML(self, address):
        pass
