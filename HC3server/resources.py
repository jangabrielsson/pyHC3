

class Resources:

    def __init__(self):
        self.globals = {}
        self.devices = {}
        self.rooms = {}
        self.sections = {}
        self.customEvents = {}

    def getGlobal(self, name):
        return self.globals.get(name)

    def createGlobal(self, name, value):
        var = {'name': name, 'value':value,'modified':0}
        self.globals[name]=var

    def setGlobal(self, name, value):
        var = {'name': name, 'value':value,'modified':0}
        self.globals[name]=var