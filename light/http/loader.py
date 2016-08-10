import os
import flask
import configparser

from light.http import dispatcher
from light.cache import Cache
from light.constant import Const
from light.model.datarider import Rider
from light.mongo.session import MongoSessionInterface

CONST = Const()


def initialize(app=None, domain=None):
    # flask
    if not app:
        app = flask.Flask(__name__)
    if not domain:
        domain = os.getenv(Const().ENV_LIGHT_APP_DOMAIN)

    # cache
    Cache(domain).init()

    # rider
    Rider.instance()

    # dispatch
    dispatcher.dispatch(app)

    # TODO: job

    # setup flask
    setup_flask(app, domain)

    # start app
    start(app)

    return app


def setup_flask(app, db):
    # setup mongodb session
    app.session_interface = MongoSessionInterface(
        db=db,
        host=os.environ[CONST.ENV_LIGHT_DB_HOST],
        port=int(os.environ[CONST.ENV_LIGHT_DB_PORT]))

    # analyse static resource
    def static(file):
        path = os.path.join(os.path.abspath('..'), 'public/static/js')
        return flask.send_from_directory(path, file)

    app.add_url_rule('/js/<path:path>', endpoint='sss', view_func=static)


def start(app):
    port = 7000
    if CONST.ENV_LIGHT_APP_PORT in os.environ:
        port = int(os.environ[CONST.ENV_LIGHT_APP_PORT])

    app.run(port=port)


def load_config_from_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # app config
    if 'app' in config:
        os.environ[CONST.ENV_LIGHT_APP_PORT] = config['app']['port']
        os.environ[CONST.ENV_LIGHT_APP_DOMAIN] = config['app']['domain']

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
