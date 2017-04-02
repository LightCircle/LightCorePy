import json

from light import helper
from http import cookies

client = {}
path = helper.project_path('controllers')
clazz = helper.resolve(name='websocket', path=path)

NAME_ACTION = 'action'
NAME_DATE = 'data'
NAME_ID = 'sid'
NAME_OPTION = 'option'


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
    action = 'message'
    if NAME_ACTION in data:
        action = data[NAME_ACTION]

    if sid in client and clazz and hasattr(clazz, action):
        handler = {
            NAME_ACTION: action,
            NAME_OPTION: client[sid],
            NAME_ID: sid
        }

        func = getattr(clazz, action)
        func(handler, data[NAME_DATE])
        return

    print('Client not found')


def send(handler=None, data=None):
    sid = handler[NAME_ID]
    if sid in client:
        client[sid]['eio'].send(
            sid,
            json.dumps({NAME_ACTION: handler[NAME_ACTION], NAME_DATE: data})
        )
        return

    print('Client not found')
