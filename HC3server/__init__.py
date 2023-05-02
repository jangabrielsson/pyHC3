from flask import Flask
import os
from HC3server.HC3 import HC3

app = Flask(__name__)

hc3 = HC3.singleton
HC3.app = app

print("Working dir:",os.getcwd())
hc3.loadAndRun("HC3server/test/mytest.lua",once=False)
hc3.loadAndRun("HC3server/test/mytest.lua",once=False)

hc3.sleep(1)
hc3.call(100,"testcall",101,2)
import HC3server.views



