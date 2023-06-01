import queue


class RefreshStates():
    events = queue.SimpleQueue()
    eid = 100
    def start():
        pass
    def stop():
        pass
    def pushEvents(self,events):
        for e in events: self.events.put(e)
    def pushEvent(self,event):
        self.events.put(event)
    def getEvents(self,id):
        pass

class RemoteRefreshStates(RefreshStates):
    pass

class LocalRefreshStates(RefreshStates):