import os
import unittest
import urllib.request
import time
import light.http.loader
import flask

from light.constant import Const

from multiprocessing import Process

CONST = Const()


class TestLoader(unittest.TestCase):
    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'
        self.app = flask.Flask(__name__)

    def test_initialize(self):
        # init application
        light.http.loader.initialize(self.app, domain='LightDB', run=False)

        # start by process
        self.app.add_url_rule('/test', endpoint='test', view_func=lambda: 'OK', methods=['GET'])
        self.server = Process(target=lambda: self.app.run(port=5000))
        self.server.start()

        # test request
        time.sleep(1)
        urllib.request.urlopen('http://127.0.0.1:5000/test?params=p1')
        time.sleep(1)

    def tearDown(self):
        # automatic stop flask server
        self.server.terminate()
        self.server.join()
