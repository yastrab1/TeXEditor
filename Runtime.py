class Runtime:
    #this is a singleton class
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    def registerData(self,key,value):
        if not hasattr(self,"data"):
            self.data = {}
        self.data[key] = value
    def getData(self,key):
        return self.data[key]