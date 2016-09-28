import os
import re
import flask
import light.helper

from light.cache import Cache
from light.constant import Const
from light.model.datarider import Rider
from light.http.context import Context
from light.configuration import Config
from light.http import response, websocket
from light.i18n import I18n

CONST = Const()
METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'GET', 'GET', 'GET', 'GET']


def dispatch(app):
    bind_api(app)
    bind_route(app)
    bind_websocket(app)


def bind_websocket(app):
    if os.getenv(CONST.ENV_LIGHT_APP_WEBSOCKET, 'on') == 'off':
        return

    from flask_uwsgi_websocket import AsyncioWebSocket
    socket = AsyncioWebSocket(app)

    async def func(ws):
        websocket.on_open(ws)
        websocket.send(ws.id, {'socketid': ws.id})
        while True:
            message = await ws.receive()
            if message is None:
                websocket.on_close(ws)
                break
            websocket.on_message(ws, message)

    socket.add_url_rule('/websocket', '/websocket', view_func=func)


def bind_api(app):
    boards = Cache.instance().get(CONST.SYSTEM_DB_BOARD)
    rider = Rider.instance()

    for board in boards:

        action = board['action']
        api = board['api']
        class_name = board['class']
        class_folder = board['path']
        method = board['type']
        print('>>>> ', api, class_name, action, METHODS[method])

        # try lookup controllers class
        path = light.helper.project_path('controllers', class_folder)
        clazz = light.helper.resolve(name=class_name, path=path)
        if clazz:
            if hasattr(clazz, action):
                add_api_rule(app, api, clazz, action, method)
                continue

        # try lookup system class
        path = light.helper.core_path('model')
        clazz = light.helper.resolve(name=class_name, path=path)
        if clazz:
            if hasattr(clazz, action):
                add_api_rule(app, api, clazz, action, method)
                continue

        # try lookup data rider
        if hasattr(rider, class_name):
            clazz = getattr(rider, class_name)
            if hasattr(clazz, action):
                add_api_rule(app, api, clazz, action, method)
                continue


def bind_route(app):
    routes = Cache.instance().get(CONST.SYSTEM_DB_ROUTE)

    for route in routes:
        action = route['action']
        url = route['url']
        class_name = route['class']
        template = route['template']
        print('>>>> ', url, action, template)

        # try lookup controllers class
        path = light.helper.project_path('controllers')
        clazz = light.helper.resolve(name=class_name, path=path)
        if clazz:
            if hasattr(clazz, action):
                add_html_rule(app, url, clazz, action, template)
                continue

        # render html
        add_html_rule(app, url, None, None, template)


def add_api_rule(app, api, clazz, action, method):
    def func(**kwargs):
        handler = Context()
        handler.extend_params(kwargs)
        data, error = getattr(clazz, action)(handler)
        return response.send(handler, data, error)

    api = re.sub('/:(\w+)', '/<\\1>', api)
    app.add_url_rule(api, endpoint=api, view_func=func, methods=[METHODS[method]])


def add_html_rule(app, url, clazz, action, template):
    def func(**kwargs):
        handler = Context()
        handler.extend_params(kwargs)

        data = dict()
        data['req'] = flask.request
        data['handler'] = handler
        data['user'] = handler.user
        data['conf'] = Config()
        data['environ'] = os.environ
        data['dynamic'] = func_dynamic
        data['csrftoken'] = flask.g.csrftoken
        data['i'] = I18n.instance().i

        if clazz:
            data['data'] = getattr(clazz, action)(handler)

        return light.helper.load_template(template).render(data)

    url = re.sub('/:(\w+)', '/<\\1>', url)
    app.add_url_rule(url, endpoint=url, view_func=func)


def func_dynamic(url):
    static = Config.instance().app.static
    stamp = Config.instance().app.stamp

    if '?' in url:
        return '{url}&stamp={stamp}'.format(static=static, url=url, stamp=stamp)

    return '{static}{url}?stamp={stamp}'.format(static=static, url=url, stamp=stamp)
