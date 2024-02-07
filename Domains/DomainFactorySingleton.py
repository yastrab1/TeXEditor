class DomainFactorySingleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DomainFactorySingleton, cls).__new__(DomainFactorySingleton)
        return cls.instance

    def createDomainByName(self, domainName: str):
        from Domains.Pmat import Pikomat, Pikofyz
        from Domains.Riesky import Riesky
        match domainName:
            case "Pikomat":
                return Pikomat()
            case "Pikofyz":
                return Pikofyz()
            case "Riesky":
                return Riesky()
            case _:
                raise Exception("Incorrect parameters passed")
