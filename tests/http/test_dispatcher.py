import os
import unittest
import flask
import light.http.dispatcher

from light.constant import Const
from light.cache import Cache

CONST = Const()


class TestDispatcher(unittest.TestCase):
    @staticmethod
    def setUpClass():
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        Cache(CONST.SYSTEM_DB).init()

    def setUp(self):
        pass

    def test_bind_app(self):
        app = flask.Flask(__name__)
        light.http.dispatcher.bind_api(app)
