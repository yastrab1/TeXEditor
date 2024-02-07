import urllib


class AbstractSeminarWebDriver:
    def __init__(self):
        self.cookies = self.authenticate()

    def authenticate(self) -> list[dict]:
        raise NotImplementedError("Not implemented")

    def getPageHTML(self, address):
        request = urllib.request.Request(address)
        for cookie in self.cookies:
            request.add_header("Cookie", f"{cookie.name}={cookie.value}")
        response = urllib.request.urlopen(request).read().decode('utf-8')
        return response

    def submitFile(self, path, year, series, number):
        raise NotImplementedError("Not implemented")
