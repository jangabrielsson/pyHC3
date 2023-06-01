import time
import json
import itertools
from HC3server import QA
from HC3server.resources import Resources
from HC3server import config

class HC3:
    def __init__(self):
        self.id = itertools.count(100)
        self.rsrc = Resources()
        self.rsrc.createGlobal("A",42)

    def sleep(self,ms):
        time.sleep(ms/1000)

    def loadAndRun(self,fname,once=True):
        qa = QA.QA(next(self.id),fname,{'value': True},once)
        self.rsrc.devices[qa.id]=qa
        qa.run()
        return qa

    def isLocalDevice (self,id):
        return self.rsrc.devices[id] != None

    def onAction(self,id,actionName,data):
        qa = self.rsrc.devices[id]
        qa.onAction(actionName,data)
    
    def call(self,id,funName,*args):
        qa = self.rsrc.devices[id]
        data = json.dumps({'args':args})
        qa.onAction(funName,data)

    
config.hc3 = HC3()