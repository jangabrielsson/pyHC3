import lupa
from lupa import LuaRuntime
from queue import PriorityQueue
import threading
import itertools
import time
from datetime import datetime
from os import path
import re
import HC3server.api as api

def api_get(url):
    return api.http_get(url)

def api_post(url, data):
    return api.http_post(url, data)

def api_post(url, data):
    return api.http_post(url, data)

def api_put(url, data):
    return api.http_put(url, data)

def api_delete(url, data):
    return api.http_delete(url, data)

def fibaro_get_global_variable(name):
    return api_get('/globalVariables/'+name)

def fibaro_get_device(id):
    return api_get('/devices/'+id)

def fibaro_get_devices():
    return api_get('/devices')

def fibaro_get_room(id):
    return api_get('/rooms/'+id)

def fibaro_get_scene(id):
    return api_get('/scenes/'+id)

def fibaro_get_device_property(id, prop):
    return api_get(f"/devices/{id}/properties/{prop}")

def fibaro_get_breached_partitions():
    return api_get('/alarms/v1/partitions/breached')

def fibaro_add_debug_message(tag, str, typ):
    typ = typ.upper()
    str = str.replace("&nbsp;", " ")          # remove html space
    time = datetime.now().strftime("[%d.%m.%Y] [%H:%M:%S]")
    print(f"{time} [{typ}] [{tag}]: {str}")

loader = '''
    function(prog,path,id,name,typ,props,hooks)
        ___id = id
        ___pyhooks = hooks
        dofile(path.."class.lua")
        json = dofile(path.."json.lua")
        dofile(path.."fibaro.lua")
        dofile(path.."quickApp.lua")
        p,err = loadfile(prog)
        if not p then error(err) 
        else 
            local stat,res = pcall(p)
            if not stat then error(res) end
            quickApp = QuickApp({id=id, name=name, type=typ, properties = props})
        end
    end
'''

hooks = {
    'api_get': api_get,
    'api_post': api_post,
    'api_put': api_put,
    'api_delete': api_delete,
    'fibaro_get_global_variable': fibaro_get_global_variable,
    'fibaro_get_device': fibaro_get_device,
    'fibaro_get_devices': fibaro_get_devices,
    'fibaro_get_room': fibaro_get_room,
    'fibaro_get_scene': fibaro_get_scene,
    'fibaro_get_device_property': fibaro_get_device_property,
    'fibaro_get_breached_partitions': fibaro_get_breached_partitions,
    'fibaro_add_debug_message': fibaro_add_debug_message
}

REMOVED = '<removed-task>'      # placeholder for a removed task


def add_task(fun, time, id, pq, entry_finder):
    'Add a new task or update the priority of an existing task'
    if id in entry_finder:
        remove_task(id)
    entry = [time, id, fun]
    entry_finder[id] = entry
    pq.put(entry)
    return id

def remove_task(id, entry_finder):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(id)
    entry[-1] = REMOVED


def pop_task(pq, entry_finder):
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        time, id, fun = pq.get()
        if time is not REMOVED:
            del entry_finder[id]
            return time, fun
# raise KeyError('pop from an empty priority queue')

class AbortableSleep():
    def __init__(self):
        self._condition = threading.Condition()

    def __call__(self, secs):
        with self._condition:
            self._aborted = False
            self._condition.wait(timeout=secs)
            return not self._aborted

    def abort(self):
        with self._condition:
            self._condition.notify()
            self._aborted = True

def netCall(url,opts,success,err):
    print(url)

class QA:
    QA_Name = re.compile("--%%name=(.+)")
    QA_Type = re.compile("--%%type=(.+)")
    def __init__(self, id, fname, props, once):
        self.fname = fname
        self.props = props
        self.once = once
        self.id = id
        self.lua = LuaRuntime(unpack_returned_tuples=True)

    def onAction(self,actionName,data):
        self._timer(lambda : self._action(self.id,actionName,data),0)
        self.sleep.abort()

    def run(self):
        def QArunner():
            pq = PriorityQueue()             # list of entries arranged in a heap
            entry_finder = {}                # mapping of tasks to entries
                  # unique sequence count
            self.sleep = AbortableSleep()
            id = itertools.count()
            f = self.lua.eval(loader)
            self._timer = lambda fun,ms : add_task(fun, ms, next(id), pq, entry_finder)
            globals = self.lua.globals()

            globals.setTimeout = lambda fun, ms: add_task(fun, time.time()+ms/1000, next(id), pq, entry_finder)
            globals.clearTimeout = lambda ref: remove_task(ref, entry_finder)
            globals['__fibaroSleep'] = lambda ms: time.sleep(ms / 1000)
            globals['__HTTP'] = lambda url,opts,success,err : netCall(url,opts,success,err)
            
            with open(self.fname) as file:
                lines = file.read()
            mt = self.QA_Type.search(lines)
            typ = mt.group(1) if mt else "com.fibaro.binarySwitch"
            mn = self.QA_Name.search(lines)
            name = mn.group(1) if mn else self.fname[0:-4]

            pth = path.join(path.dirname(__file__),"lua","")
            
            try:
                f(self.fname, pth, self.id, name, typ, self.lua.table(self.props), self.lua.table_from(hooks))
            except Exception as err:
                print(err)

            self._action = globals['__onAction']

            try:
                while True:
                    if not pq.empty() > 0:
                        t, fun = pop_task(pq, entry_finder)
                        if self.sleep(max(t-time.time(), 0)):
                            try:
                             fun()
                            except Exception as x:
                                print(x)
                        else:
                            add_task(fun, t, next(id), pq, entry_finder)
                    elif self.once==True:
                        return
            except StopIteration:
                print("OK")
        self.thread = threading.Thread(target=QArunner, args=())
        self.thread.start()
