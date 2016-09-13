import json
from light import helper

client = {}
path = helper.project_path('controllers')
clazz = helper.resolve(name='websocket', path=path)


def on_open(ws):
    client[ws.id] = ws


def on_close(ws):
    del client[ws.id]


def on_message(ws, message):
    if clazz and hasattr(clazz, 'onmessage'):
        onmessage = getattr(clazz, 'onmessage')
        onmessage(ws.id, json.loads(message))


def send(cid, message=None):
    if cid in client:
        client[cid].send_nb(json.dumps({'data': message}))
