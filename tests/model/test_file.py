import os
import unittest

from light.constant import Const
from light.model.datarider import Rider
from light.cache import Cache
from light.http.context import Context

CONST = Const()


class TestFile(unittest.TestCase):

    @staticmethod
    def setUpClass():
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        Cache(CONST.SYSTEM_DB).init()

    def setUp(self):
        self.handler = Context(uid='000000000000000000000001', domain='LightDB', code='light')
        self.rider = Rider.instance()

    def test_upload(self):
        pass
