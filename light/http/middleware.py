import flask
import re

from flask import request, session
from light.configuration import Config
from light import helper


def setup(app):
    config = Config.instance()

    @app.before_request
    def authenticate():
        if request.path.startswith('/static/'):
            return

        for ignore in config.ignore.auth:
            if re.match(ignore, request.path):
                return

        if 'user' in session:
            return

        if helper.is_browser(request.headers):
            return flask.redirect(config.app.home)

        flask.abort(401)

    @app.before_request
    def csrftoken():
        flask.g.csrftoken = generate_csrf_token()

        if request.method not in ['POST', 'PUT', 'DELETE']:
            return

        for ignore in config.ignore.csrf:
            if re.match(ignore, request.path):
                return

        if request.values['_csrf'] == session['csrftoken']:
            return

        flask.abort(403)

    @app.before_request
    def policy():
        pass

    @app.before_request
    def validator():
        pass

    @app.before_request
    def permission():
        pass


def generate_csrf_token():
    if 'csrftoken' in session:
        return session['csrftoken']

    session['csrftoken'] = helper.random_guid(size=12)
    return session['csrftoken']
