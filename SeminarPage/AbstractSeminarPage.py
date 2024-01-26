class AbstractSeminarPage:
    def authenticate(self):
        raise NotImplementedError("Not implemented")

    def getPageHTML(self, address):
        raise NotImplementedError("Not implemented")

    def submitFile(self, path, year, series, number):
        raise NotImplementedError("Not implemented")
