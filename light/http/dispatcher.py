import os
import flask
import light.helper

from light.cache import Cache
from light.constant import Const
from light.model.datarider import Rider
from light.http.context import Context
from light.configuration import Config

CONST = Const()


def dispatch(app):
    bind_api(app)
    bind_route(app)


def bind_api(app):
    boards = Cache.instance().get(CONST.SYSTEM_DB_BOARD)
    rider = Rider.instance()

    for board in boards:

        action = board['action']
        api = board['api']
        class_name = board['class']
        class_folder = board['path']

        # try lookup controllers class
        path = light.helper.project_path('controllers', class_folder)
        clazz = light.helper.resolve(name=class_name, path=path)
        if clazz:
            if hasattr(clazz, action):
                add_api_rule(app, api, clazz, action)
                continue

        # try lookup system class
        path = light.helper.core_path('model')
        clazz = light.helper.resolve(name=class_name, path=path)
        if clazz:
            if hasattr(clazz, action):
                add_api_rule(app, api, clazz, action)
                continue

        # try lookup data rider
        clazz = getattr(rider, class_name)
        if clazz:
            if hasattr(clazz, action):
                add_api_rule(app, api, clazz, action)
                continue


def bind_route(app):
    routes = Cache.instance().get(CONST.SYSTEM_DB_ROUTE)

    for route in routes:
        action = route['action']
        url = route['url']
        class_name = route['class']
        template = route['template']
        print(url, action, template)

        # try lookup controllers class
        path = light.helper.project_path('controllers')
        clazz = light.helper.resolve(name=class_name, path=path)
        if clazz:
            if hasattr(clazz, action):
                add_html_rule(app, url, clazz, action, template)
                continue

        # render html
        add_html_rule(app, url, None, None, template)


def add_api_rule(app, api, clazz, action):
    def func():
        return flask.jsonify(getattr(clazz, action)(Context())), 200

    app.add_url_rule(api, endpoint=api, view_func=func)


def add_html_rule(app, url, clazz, action, template):
    def func():
        handler = Context()
        data = dict()
        data['req'] = flask.request
        data['handler'] = handler
        data['user'] = handler.user
        data['conf'] = Config()
        data['environ'] = os.environ
        data['dynamic'] = func_dynamic

        if clazz:
            data['data'] = getattr(clazz, action)(handler)

        return light.helper.load_template(template).render(data)

    app.add_url_rule(url, endpoint=url, view_func=func)


def func_dynamic(url):

    if '?' in url:
        return '{url}&stamp={stamp}'.format(url=url, stamp=Config.instance().app.stamp)

    return '{url}?stamp={stamp}'.format(url=url, stamp=Config.instance().app.stamp)
