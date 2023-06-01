from flask import Flask
from flask import request, Response
from flask import g
import requests
from requests.exceptions import ConnectTimeout
import json
from HC3server import app, HC3
from HC3server import config
from HC3server import QA

API_HOST = "http://192.168.1.57"


def forward(req):
    try:
        res = requests.request(  # ref. https://stackoverflow.com/a/36601467/248616
            method=request.method,
            url=request.url.replace(request.host_url, f'{API_HOST}/'),
            headers=request.headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=5,
        )
    except ConnectTimeout as e:
        return app.response_class(
            response="nil",
            status=505,
            mimetype='application/json'
        )

    return app.response_class(
        response=res.content,
        status=res.status_code,
        mimetype='application/json'
    )


@app.route('/')
def hello():
    return 'Hello, World!'

# devices


@app.post('/api/devices/<int:id>/action/<actionName>')
def action(id, actionName):
    '''Call QA method'''
    if config.hc3.isLocalDevice(id):
        data = request.data.decode('UTF-8')
        config.hc3.onAction(id, actionName, data)
        return {'message': "Accepted"}
    else:
        return forward(request)


@app.get('/api/callAction')
def callAction():
    '''Call QA method'''
    return {'message': "Accepted"}


@app.get('/api/devices')
def getDevices():
    '''Return all devices'''
    return {}                       # support selectors


@app.get('/api/devices/<int:id>')
def getDevice(id):
    '''Return specific device'''
    if config.hc3.isLocalDevice(id):
        return {}
    else:
        return forward(request)


@app.get('/api/devices/<int:id>/properties/<prop>')
def getDeviceProp(id, prop):
    '''Return device property'''
    if config.hc3.isLocalDevice(id):
        return {'message': "Accepted"}
    else:
        return forward(request)


@app.put('/api/devices/<int:id>')
def setDevice(id):
    '''Modify device'''
    if config.hc3.isLocalDevice(id):
        return {'message': "Accepted"}
    else:
        return forward(request)

# globalVariables


@app.get('/api/globalVariables')
def getGlobalVariables():
    '''Get all global variables'''
    return forward(request)


@app.get('/api/globalVariables/<name>')
def getGlobalVariable(name):
    '''Get all global variables'''
    var = config.hc3.rsrc.getGlobal(name)
    if var != None:
        return var
    else:
        return forward(request)


@app.post('/api/globalVariables')
def createGlobalVariable():
    '''Create global variable'''
    return forward(request)


@app.put('/api/globalVariables/<name>')
def setGlobalVariable(name):
    '''Set global variable'''
    return forward(request)


@app.delete('/api/globalVariables/<name>')
def deleteGlobalVariable(name):
    '''Delete global variable'''
    return forward(request)

# rooms


@app.get('/api/rooms')
def getRooms():
    '''Get all rooms'''
    if config.hc3.isLocalRoom(id):
        return {'message': "Accepted"}
    else:
        return forward(request)


@app.get('/api/rooms/<int:id>')
def getRoom(id):
    '''Get specific room'''
    return forward(request)


@app.post('/api/rooms')
def createRoom():
    '''Create room'''
    return forward(request)


@app.post('/api/rooms/<int:id>/action/setAsDefault')
def setRoomAsDefault(id):
    '''Set default room'''
    return forward(request)


@app.put('/api/rooms/<int:id>')
def setRoom(id):
    '''Modify room'''
    return forward(request)


@app.delete('/api/rooms/<int:id>')
def deleteRoom(id):
    '''Delete room'''
    return forward(request)

# sections


@app.get('/api/sections')
def getSections():
    '''Get all sections'''
    return forward(request)


@app.get('/api/sections/<int:id>')
def getSection(id):
    '''Get specific section'''
    return forward(request)

@app.post('/api/sections')
def createSection():
    '''Modify section'''
    return forward(request)


@app.put('/api/sections/<int:id>')
def setSection(id):
    return forward(request)


@app.delete('/sections/<int:id>')
def deleteSection(id):
    return forward(request)

# customEvents


@app.get('/api/customEvents')
def getCustomEvents():
    return forward(request)


@app.get('/api/customEvents/<name>')
def getCustomEvent(name):
    return forward(request)


@app.post('/api/customEvents')
def createCustomEvent():
    return forward(request)


@app.post('/api/customEvents/<name>')
def emitCustomEvent(name):
    return forward(request)


@app.put('/api/customEvents/<name>')
def setCustomEvent(name):
    return forward(request)


@app.delete('/api/customEvents/<name>')
def deleteCustomEvent(name):
    return forward(request)

# scenes


@app.get('/api/scenes')
def getScenes():
    return forward(request)


@app.get('/api/scenes/<int:id>')
def getScene(id):
    return forward(request)

# plugins


@app.post('/api/plugins/updateProperty')
def updateProperty():
    return forward(request)


@app.post('/api/plugins/updateView')
def updateView():
    return forward(request)


@app.post('/api/plugins/restart')
def restartQA():
    return forward(request)


@app.post('/api/plugins/createChildDevice')
def createChild():
    return forward(request)


@app.post('/api/debugMessages')
def debuMessage():
    return forward(request)


@app.post('/api/plugins/publishEvent')
def publishEvent():
    return forward(request)


@app.delete('/api/plugins/removeChildDevice/<int:id>')
def removeChild(id):
    return forward(request)

# location


@app.get('/api/panels/location')
def getLocations():
    return forward(request)


@app.get('/api/panels/location/<int:id>')
def getLocation(id):
    return forward(request)


@app.post('/api/panels/location')
def createLocation():
    return forward(request)


@app.put('/api/panels/location/<int:id>')
def setLocation():
    return forward(request)


@app.delete('/api/panels/location/<int:id>')
def deleteLocation():
    return forward(request)

# users


@app.get('/api/users')
def getUsers():
    '''Get all users'''
    return forward(request)


@app.get('/api/users/<int:id>')
def getUser(id):
    '''Get specific user'''
    return forward(request)


@app.post('/api/users')
def createUser():
    '''Create user'''
    return forward(request)


@app.put('/api/users/<int:id>')
def modifyUser(id):
    '''Modify user'''
    return forward(request)


@app.delete('/api/users/<int:id>')
def deleteUser(id):
    '''Delete user'''
    return forward(request)

# quickApp


@app.get('/api/quickApp/<int:id>/files')
def getFiles(id):
    '''Get QA files'''
    return forward(request)


@app.post('/api/quickApp/<int:id>/files')
def createFiles(id):
    '''Create QA files'''
    return forward(request)


@app.get('/api/quickApp/<int:id>/files/<name>')
def getFile(id, name):
    '''Get specific QA file'''
    return forward(request)


@app.put('/api/quickApp/<int:id>/files/<name>')
def updateFile(id, name):
    '''Update specific QA file'''
    return forward(request)


@app.put('/api/quickApp/<int:id>/files')
def updateFiles(id):
    '''Update QA files'''
    return forward(request)


@app.get('/api/quickApp/export/<int:id>')
def exportQA(id):
    '''Export QA to .fqa'''
    return forward(request)


@app.post('/api/quickApp/')
def installQA():
    '''Install QA'''
    return forward(request)


@app.delete('/api/quickApp/<int:id>/files/<name>')
def deleteFile(id, name):
    '''Delete QA file'''
    return forward(request)


@app.get('/api/plugins/<int:id>/variables')
def getKeys(id):
    '''Get all QA keys'''
    return forward(request)


@app.get('/api/plugins/<int:id>/variables/<name>')
def getKey(id, name):
    '''Get QA key value'''
    return forward(request)


@app.post('/api/plugins/<int:id>/variables')
def createKey(id):
    '''Create QA key'''
    return forward(request)


@app.put('/api/plugins/<int:id>/variables/<name>')
def pluginsSetVariable(id, name):
    '''Create QA files'''
    return forward(request)


@app.delete('/api/plugins/<int:id>/variables/<name>')
def deleteKey(id, name):
    '''Delete QA key'''
    return forward(request)


@app.delete('/api/plugins/<int:id>/variables')
def deleteKeys(id):
    '''Delete all QA keys'''
    return forward(request)
