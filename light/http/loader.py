import os
import flask
import configparser
import engineio
import gevent.pywsgi
import geventwebsocket.handler

from light import helper
from light.http import dispatcher, middleware
from light.cache import Cache
from light.constant import Const
from light.model.datarider import Rider
from light.mongo.session import MongoSessionInterface
from light.configuration import Config
from light.job import Schedule
from light.log import Log

CONST = Const()


def initialize(app=None, domain=None):
    # logging
    Log.init()

    # flask
    if not app:
        app = flask.Flask(__name__)

    if not domain:
        domain = os.getenv(CONST.ENV_LIGHT_APP_DOMAIN)

    # cache
    db = Cache(domain).init()

    # rider
    Rider.instance()

    # TODO: job
    Schedule().start()

    # setup flask
    eio = setup_flask(app, db)

    # If you set the environment variable websocket to off, then eio = null
    if eio:
        return engineio.Middleware(eio, app)
    return app


def setup_flask(app, db):
    # setup mongodb session
    app.session_interface = MongoSessionInterface(db=db)

    # analyse static resource
    app.static_folder = helper.project_path() + Config.instance().app.static
    app.static_url_path = Config.instance().app.static

    # setup middleware
    middleware.setup(app)

    # dispatch
    return dispatcher.dispatch(app)


def start_server(app):
    host = '0.0.0.0'
    port = int(os.environ[Const().ENV_LIGHT_APP_PORT])
    server = gevent.pywsgi.WSGIServer((host, port), app, handler_class=geventwebsocket.handler.WebSocketHandler)
    server.serve_forever()


def load_config_from_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # app config
    if 'app' in config:
        os.environ[CONST.ENV_LIGHT_APP_PORT] = config['app']['port']
        os.environ[CONST.ENV_LIGHT_APP_DOMAIN] = config['app']['domain']
        os.environ[CONST.ENV_LIGHT_APP_DEV] = config['app']['dev']
        os.environ[CONST.ENV_LIGHT_APP_MASTER] = config['app']['master']
        os.environ[CONST.ENV_LIGHT_APP_LOCAL] = config['app']['local']

    # mongodb config
    if 'mongodb' in config:
        os.environ[CONST.ENV_LIGHT_DB_HOST] = config['mongodb']['host']
        os.environ[CONST.ENV_LIGHT_DB_PORT] = config['mongodb']['port']
        os.environ[CONST.ENV_LIGHT_DB_USER] = config['mongodb']['user']
        os.environ[CONST.ENV_LIGHT_DB_PASS] = config['mongodb']['pass']
        os.environ[CONST.ENV_LIGHT_DB_AUTH] = config['mongodb']['auth']

    # mysql config
    if 'mysql' in config:
        os.environ[CONST.ENV_LIGHT_MYSQL_HOST] = config['mysql']['host']
        os.environ[CONST.ENV_LIGHT_MYSQL_PORT] = config['mysql']['port']
        os.environ[CONST.ENV_LIGHT_MYSQL_USER] = config['mysql']['user']
        os.environ[CONST.ENV_LIGHT_MYSQL_PASS] = config['mysql']['pass']
