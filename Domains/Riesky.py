import re

from Domains.Domain import Domain


class Riesky(Domain):
    def __init__(self):
        super().__init__()
        self.summaryPatter = re.compile("Riešky (\\d.)\\.séria, (.)? séria")

    def getSeriesNumberFromEventSummaryIfCorrect(self, event):
        match = self.summaryPatter.match(event.summary)
        if match:
            relativeSeries = int(match.group(1))
            season = match.group(2)
            return relativeSeries + self.getModifierBySeason(season)

    def getModifierBySeason(self, season):
        return 0 if season == "zimná" else 3

    def getName(self) -> str:
        pass
