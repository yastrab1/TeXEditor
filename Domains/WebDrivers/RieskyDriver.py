import os.path
import urllib

from bs4 import BeautifulSoup
from mechanize import *

from Config.Config import Config
from Domains.WebDrivers.AbstractSeminarPage import AbstractSeminarWebDriver


def _getCurrentPartOfYear(seriesNum):
    return "zimna" if seriesNum < 3 else "letna"


class RieskyDriver(AbstractSeminarWebDriver):
    def __init__(self):
        super().__init__()
        self.browser = Browser()

    def authenticate(self) -> list[dict]:
        self.browser.open("https://riesky.sk/ucet/prihlasenie")
        self.browser.select_form(method="POST")
        print(Config().get("RieskyPassword"))
        self.browser["username"] = Config().get("RieskyUsername")
        self.browser["password"] = Config().get("RieskyPassword")
        self.browser.submit()
        cookiesList = self.cookiejarToCookieList()
        return cookiesList

    def cookiejarToCookieList(self):
        cookies_list = []
        for cookie in self.browser.cookie_jar:
            cookie_dict = {
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires,
                'secure': cookie.secure,
                'httponly': cookie._rest['HttpOnly'] if 'HttpOnly' in cookie._rest else None,
            }
            cookies_list.append(cookie_dict)
        return cookies_list

    def getPageHTML(self, linkAddr):
        request = urllib.request.Request(linkAddr)
        for cookie in self.cookies:
            request.add_header("Cookie", f"{cookie.name}={cookie.value}")
        response = urllib.request.urlopen(request).read().decode('utf-8')
        return response

    def submitFile(self, path, year, series, number):
        self.browser.open(
            f"https://riesky.sk/rocnik/{year}/{_getCurrentPartOfYear(series)}/kolo/{series % 3 + 1}/priklad/{number}/odovzdavanie/")
        self.browser.select_form(nr=2)
        self.browser.form.add_file(open(path, 'rb'), 'application/pdf', os.path.basename(path))
        self.browser.submit()


class RieskyScraper:
    def __init__(self):
        self.page = RieskyDriver()
        self.page.authenticate()

    def getExercisesFromSeriesAndYear(self, seriesNum, year):
        partOfYear = self._getCurrentPartOfYear(seriesNum)
        html = self.page.getPageHTML(f"https://riesky.sk/rocnik/{year}/{partOfYear}/kolo/{seriesNum % 3 + 1}/zadania/")
        soup = BeautifulSoup(html, features="html5lib")
        result = []
        for exercise in soup.find_all("div", class_="zadanie"):
            result.append(exercise)
        return result

    def getPointsFromSeries(self, series, year):
        partOfYear = self._getCurrentPartOfYear(series)

        html = self.page.getPageHTML("https://riesky.sk/moje_riesenia/")
        soup = BeautifulSoup(html, features="html5lib")
        seriesCard = soup.find("div", {"id": f"collapse-{year}-{partOfYear}-{series % 3 + 1}"})
        for card in seriesCard.find_all("tr", class_="table-success"):
            print(card.contents[7].text)

    def _getCurrentPartOfYear(self, series) -> str:
        return "zimna" if series < 3 else "letna"
