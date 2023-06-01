from flask import Flask
from flask.testing import FlaskClient
import os
from HC3server import config
from HC3server import HC3

app = Flask(__name__)
config.app = app
config.client = app.test_client() #FlaskClient(config.app)

print("Working dir:",os.getcwd())
import HC3server.views

config.hc3.loadAndRun("HC3server/test/mytest.lua",once=False)
config.hc3.loadAndRun("HC3server/test/mytest.lua",once=False)

config.hc3.sleep(1)
config.hc3.call(100,"testcall",101,2)



