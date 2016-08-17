import os
import unittest
import flask
import time

from light.job import Schedule
from light.constant import Const
from multiprocessing import Process

CONST = Const()


class TestJob(unittest.TestCase):
    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'
        self.app = flask.Flask(__name__)

    def test_start(self):
        self.server = Process(target=lambda: self.app.run(port=5000))
        self.server.start()

        Schedule().start()
        time.sleep(3)

    def tearDown(self):
        self.server.terminate()
        self.server.join()
        pass
