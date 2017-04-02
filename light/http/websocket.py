import json

from light import helper
from http import cookies

client = {}
path = helper.project_path('controllers')
clazz = helper.resolve(name='websocket', path=path)


def connect(sid, eio, environ=None):
    # TODO: check auth(cookie)

    cookie = cookies.SimpleCookie(environ['HTTP_COOKIE'])
    if cookie and 'session' in cookie:
        client[sid] = {
            'sid': sid,
            'cid': cookie['session'].value,
            'eio': eio,
            'environ': environ
        }


def disconnect(sid):
    del client[sid]


def message(sid, data):
    if sid in client and clazz and hasattr(clazz, 'message'):
        func = getattr(clazz, 'message')
        func(data, client[sid])
        return

    print('Client not found')


def send(sid, data=None):
    if sid in client:
        client[sid]['eio'].send(sid, json.dumps(data))
        return

    print('Client not found')
