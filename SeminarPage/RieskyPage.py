import urllib

from bs4 import BeautifulSoup
from mechanize import *

from Config.Config import Config


class RieskyPage:
    def __init__(self):
        self.browser = Browser()

    def logIn(self):
        self.browser.open("https://riesky.sk/ucet/prihlasenie")
        self.browser.select_form(method="POST")
        self.browser["username"] = Config().get("RieskyUsername")
        self.browser["password"] = Config().get("RieskyPassword")
        self.browser.submit()
        self.cookies = [i for i in self.browser.cookiejar]

    def getPageHTML(self, linkAddr):
        request = urllib.request.Request(linkAddr)
        for cookie in self.cookies:
            request.add_header("Cookie", f"{cookie.name}={cookie.value}")
        response = urllib.request.urlopen(request).read().decode('utf-8')
        return response


class RieskyScraper:
    def __init__(self):
        self.page = RieskyPage()
        self.page.logIn()

    def getExercisesFromSeriesAndYear(self, seriesNum, year):
        partOfYear = self.getCurrentPartOfYear(seriesNum)
        html = self.page.getPageHTML(f"https://riesky.sk/rocnik/{year}/{partOfYear}/kolo/{seriesNum % 3 + 1}/zadania/")
        soup = BeautifulSoup(html, features="html5lib")
        result = []
        for exercise in soup.find_all("div", class_="zadanie"):
            result.append(exercise)
        return result

    def getCurrentPartOfYear(self, seriesNum):
        return "zimna" if seriesNum <= 3 else "letna"

    def getPointsFromSeries(self, series, year):
        partOfYear = self.getCurrentPartOfYear(series)

        html = self.page.getPageHTML("https://riesky.sk/moje_riesenia/")
        soup = BeautifulSoup(html, features="html5lib")
        seriesCard = soup.find("div", {"id": f"collapse-{year}-{partOfYear}-{series % 3 + 1}"})
        for card in seriesCard.find_all("tr", class_="table-success"):
            print(card.contents[7].text)
