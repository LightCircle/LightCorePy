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
    setup_flask()

    # start app
    start(app)


def setup_flask(app):
    # 初始化基于mongo的session
    app.session_interface = MongoSessionInterface(
        db='sessions',
        port=os.environ[CONST.ENV_LIGHT_DB_PORT],
        host=os.environ[CONST.ENV_LIGHT_DB_HOST])

    # 解析静态资源
    def static(file):
        path = os.path.join(os.path.abspath('..'), 'public/static/js')
        return flask.send_from_directory(path, file)

    app.add_url_rule('/js/<path:path>', endpoint='sss', view_func=static)


def start(app):
    app.run()
