import urllib

from bs4 import BeautifulSoup
from mechanize import *


class RieskyPage:
    def __init__(self):
        self.browser = Browser()

    def logIn(self):
        self.browser.open("https://riesky.sk/ucet/prihlasenie")
        self.browser.select_form(method="POST")
        self.browser["username"] = ""
        self.browser["password"] = ""
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
        partOfYear = "zimna" if seriesNum <= 3 else "letna"
        html = self.page.getPageHTML(f"https://riesky.sk/rocnik/{year}/{partOfYear}/kolo/{seriesNum % 3 + 1}/zadania/")
        soup = BeautifulSoup(html, features="html5lib")
        result = []
        for exercise in soup.find_all("div", class_="zadanie"):
            result.append(exercise)
        return result

    def getPointsFromCurrentSeries(self):
        html = self.page.getPageHTML("https://riesky.sk/moje_riesenia/")
        soup = BeautifulSoup(html, features="html5lib")
        currentSeries = soup.find("div", class_="card-body")
        for card in currentSeries.find_all("tr", class_="table-success"):
            print(card.contents[7].text)
