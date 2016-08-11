import os
import unittest

from light.constant import Const
from light.cache import Cache
from light.http.context import Context
from light.model.datarider import Rider
from light.model.user import User

CONST = Const()


class TestUser(unittest.TestCase):
    @staticmethod
    def setUpClass():
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        Cache(CONST.SYSTEM_DB).init()

    def setUp(self):
        self.handler = Context(
            uid='000000000000000000000001',
            domain='LightDB',
            code='light',
            param={}
        )
        self.handler.set_code(Const.DEFAULT_TENANT)
        self.rider = Rider.instance()

    def test_verify(self):
        user = User()

        self.handler.params.id = 'admin'
        self.handler.params.password = '1qaz2wsx'
        u, e = user.verify(self.handler)

        self.assertIsNone(e)
        self.assertIsNotNone(u)
