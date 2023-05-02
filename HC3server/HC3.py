import time
import json
import itertools
from lupa import LuaRuntime as Lua
import HC3server.QA as QA

lua = Lua()

class HC3:
    def __init__(self):
        self.id = itertools.count(100)
        self.devices = {}

    def sleep(self,ms):
        time.sleep(ms/1000)

    def loadAndRun(self,fname,once=True):
        qa = QA.QA(next(self.id),fname,{'value': True},once)
        self.devices[qa.id]=qa
        qa.run()
        return qa

    def isLocalDevice (self,id):
        return self.devices[id] != None

    def onAction(self,id,actionName,data):
        qa = self.devices[id]
        qa.onAction(actionName,data)
    
    def call(self,id,funName,*args):
        qa = self.devices[id]
        data = json.dumps({'args':args})
        qa.onAction(funName,data)
    
HC3.singleton = HC3()