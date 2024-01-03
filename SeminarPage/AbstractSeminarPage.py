class AbstractSeminarPage:
    def authenticate(self):
        raise NotImplementedError("Not implemented")

    def getPageHTML(self, address):
        raise NotImplementedError("Not implemented")

    def submitFile(self, address, formId, filePath):
        raise NotImplementedError("Not implemented")
