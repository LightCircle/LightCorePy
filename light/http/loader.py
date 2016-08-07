import os
import flask

from light.cache import Cache
from light.mongo.session import MongoSessionInterface
from light.constant import Const

CONST = Const()


def initialize(app, domain):
    # cache
    Cache(domain).init()

    # rider

    # job

    # setup flask
    setup_flask(app)

    # start app
    # start(app)


def setup_flask(app):
    # setup mongodb session
    app.session_interface = MongoSessionInterface(
        db='sessions1',
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
