import os
import unittest
import time
import light.http.loader

from light.constant import Const
from flask import Flask
from multiprocessing import Process

CONST = Const()


class TestLoader(unittest.TestCase):
    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'
        self.app = Flask(__name__)

    def test_initialize(self):
        # init application
        light.http.loader.initialize(self.app, 'LightDB')

        # start by process
        def run():
            self.app.run()

        self.server = Process(target=run)
        self.server.start()
        time.sleep(1)

    def tearDown(self):
        # automatic stop flask server
        self.server.terminate()
        self.server.join()
