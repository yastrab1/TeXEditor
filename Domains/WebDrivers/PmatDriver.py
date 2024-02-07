import urllib

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Config.Config import Config
from Domains.WebDrivers.AbstractSeminarPage import AbstractSeminarWebDriver


class PmatDriver(AbstractSeminarWebDriver):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def authenticate(self) -> list[dict]:
        self.driver.get(self.getURL())
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

        return self.driver.get_cookies()

    def getURL(self):
        raise NotImplementedError("This is superclass that should be derived")

    def getPageHTML(self, address):
        request = urllib.request.Request(address)
        for cookie in self.cookies:
            request.add_header("Cookie", f"{cookie.name}={cookie.value}")
        response = urllib.request.urlopen(request).read().decode('utf-8')
        return response


class PikomatDriver(PmatDriver):
    def getURL(self):
        return "https://pikomat.sk/"


class PikofyzDriver(PmatDriver):
    def getURL(self):
        return "https://pikofyz.sk/"
