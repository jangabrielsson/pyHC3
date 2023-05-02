from flask import request
import json
import requests
from requests.auth import HTTPBasicAuth

configs = {
    'host': '127.0.0.1:5000', #"192.168.1.57" 
    'user': 'admin',
    'pwd': 'admin'
}

headers = {
    'Accept': "*/*",
    'Content-type': "application/json",
    'X-Fibaro-Version': '2',
}

def config(host, user, pwd):
    configs['host'] = host
    configs['user'] = user
    configs['pwd'] = pwd


def http_get(path):
    res = requests.get(f"http://{configs['host']}/api{path}",
                       auth=HTTPBasicAuth(configs['user'], configs['pwd']),
                       headers=headers)
    if res.status_code < 300:
        return res.text,res.status_code
    else:
        return None, res.status_code


def http_put(path, data):
    res = requests.put(f"http://{configs['host']}/api{path}",
                       auth=HTTPBasicAuth(configs['user'], configs['pwd']),
                       headers=headers,
                       data=data)
    return None, res.status_code


def http_post(path, data):
    res = requests.post(f"http://{configs['host']}/api{path}",
                       auth=HTTPBasicAuth(configs['user'], configs['pwd']),
                       headers=headers,
                       data=data)
    return None, res.status_code


def http_delete(path, data):
    res = requests.delete(f"http://{configs['host']}/api{path}",
                       auth=HTTPBasicAuth(configs['user'], configs['pwd']),
                       headers=headers,
                       data=data)
    return None, res.status_code