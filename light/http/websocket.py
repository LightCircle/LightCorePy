import json
import gevent

from http import cookies
from light import helper
from light.http.context import Context

clients = {}
clazz_path = helper.project_path('controllers')
clazz = helper.resolve(name='websocket', path=clazz_path)


def connect(sid, eio, session, environ=None):
    # TODO: check auth(cookie)
    # TODO: session cache to memory

    cookie = cookies.SimpleCookie(environ['HTTP_COOKIE'])

    if session:
        clients[sid] = {
            'sid': sid,
            'eio': eio,
            'cid': cookie['session'].value,
            'session': session,
            'environ': environ
        }


def disconnect(sid):
    del clients[sid]


def message(sid, data):
    action = 'message'
    if 'action' in data:
        action = data['action']

    if sid in clients and clazz and hasattr(clazz, action):
        handler = SocketContext(sid, clients[sid]['cid'], action, clients[sid]['session'])
        handler.set_params(data['data'])

        func = getattr(clazz, action)
        func(handler)
        return

    print('Client not found')


def send(handler, data=None):

    for key in list(clients):
        client = clients[key]
        if client and client['cid'] == handler.cid:
            client['eio'].send(
                client['sid'],
                json.dumps({'action': handler.action, 'data': data})
            )
            gevent.sleep(0)
            print('Send message to client : {0}, {1}'.format(handler.cid, client['sid']))


def send_to(handler, data=None):

    if handler.sid in clients:
        clients[handler.sid]['eio'].send(
            handler.sid,
            json.dumps({'action': handler.action, 'data': data})
        )
        return

    print('Client not found')


def create_session(app, cookie):
    request = SimpleRequest(cookie)
    return app.session_interface.open_session(app, request)


class SocketContext(Context):
    def __init__(self, sid, cid, action, session):
        super().__init__(session['user']['_id'], session['domain'], session['code'], {})
        self._sid = sid         # socket connect id
        self._cid = cid         # client id (session id)
        self._action = action   # request action
        self.session = session  # user session

    def get_cid(self):
        return self._cid

    def get_sid(self):
        return self._sid

    def get_action(self):
        return self._action

    cid = property(fget=get_cid)
    sid = property(fget=get_sid)
    action = property(fget=get_action)


class Cookies(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, key):
        return self.cookie[key].value


class SimpleRequest(object):
    def __init__(self, cookie):
        self.cookies = Cookies(cookie)
