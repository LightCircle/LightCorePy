import os
import unittest
import flask
import time
import urllib.request
import light.http.dispatcher

from multiprocessing import Process
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

        # change work dir
        os.chdir(os.path.abspath('../..'))

    def setUp(self):
        pass

    def test_bind_app(self):
        app = flask.Flask(__name__)
        light.http.dispatcher.dispatch(app)

        # start by process
        def app_run():
            app.run(port=5000)

        self.server = Process(target=app_run)
        self.server.start()

        time.sleep(1)

        urllib.request.urlopen('http://127.0.0.1:5000/api/app/add')
        urllib.request.urlopen('http://127.0.0.1:5000/')

    def tearDown(self):
        # automatic stop flask server
        self.server.terminate()
        self.server.join()
