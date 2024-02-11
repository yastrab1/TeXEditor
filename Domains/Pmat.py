import datetime
import re

from Domains.Domain import Domain
from Domains.WebDrivers.PmatDriver import PmatDriver


class Pmat(Domain):
    def __init__(self):
        super().__init__()
        self.summaryPattern = re.compile(self.getName()+r" (\d+)\.séria")

    def getSeriesNumberFromEventSummaryIfCorrect(self, event):
        match = self.summaryPattern.fullmatch(event.summary)
        if match:
            relativeSeries = int(match.group(1))
            return relativeSeries + self.getSeasonalModifier()

    def getSeasonalModifier(self) -> int:
        return 0 if datetime.datetime.today().month <= 6 else 3


class Pikomat(Pmat):
    def __init__(self):
        super().__init__()
        self.webDriver = PmatDriver()

    def getName(self) -> str:
        return "Pikomat"


class Pikofyz(Pmat):
    def getName(self) -> str:
        return "Pikofyz"
