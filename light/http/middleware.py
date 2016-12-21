import flask
import re

from flask import request, session
from light.configuration import Config
from light import helper
from light.i18n import I18n

COOKIE_KEY_LANG = 'light.lang'
COOKIE_KEY_ACCEPT_LANGUAGE = 'Accept-Language'
SESSION_KEY_CSRF_TOKEN = 'csrftoken'
SESSION_KEY_USER = 'user'


def setup(app):
    config = Config.instance()

    @app.before_request
    def lang():
        # The cookie takes precedence
        ua_lang = request.cookies.get(COOKIE_KEY_LANG)

        if not ua_lang:
            # Ping flask for available languages
            ua_lang = request.headers.get(COOKIE_KEY_ACCEPT_LANGUAGE)
            if ua_lang:
                ua_lang = ua_lang.split(',')[0]

        I18n.instance().lang = ua_lang or 'zh'
        flask.g.lang = ua_lang or 'zh'

    @app.before_request
    def authenticate():
        if request.path.startswith('/static/'):
            return

        for ignore in config.ignore.auth:
            if re.match(ignore, request.path):
                return

        if SESSION_KEY_USER in session:
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

        if '_csrf' in request.values:
            if request.values['_csrf'] == session[SESSION_KEY_CSRF_TOKEN]:
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

    @app.after_request
    def set_lang(response):
        response.set_cookie(COOKIE_KEY_LANG, flask.g.lang)
        return response


def generate_csrf_token():
    if SESSION_KEY_CSRF_TOKEN in session:
        return session[SESSION_KEY_CSRF_TOKEN]

    session[SESSION_KEY_CSRF_TOKEN] = helper.random_guid(size=12)
    return session[SESSION_KEY_CSRF_TOKEN]
