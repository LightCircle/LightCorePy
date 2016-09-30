import os
import unittest
import light.model.data

from light.constant import Const
from light.model.datarider import Data
from light.cache import Cache
from light.http.context import Context

CONST = Const()


class TestData(unittest.TestCase):
    @staticmethod
    def setUpClass():
        os.environ[CONST.ENV_LIGHT_DB_HOST] = '127.0.0.1'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        # Cache(CONST.SYSTEM_DB).init()

    def test_get_order(self):
        self.handler.params.sort = {'schema': 'desc', 'field': 'asc'}
        result = light.model.data.get_order(self.handler, self.board)
        print(result)

    def setUp(self):
        self.handler = Context(uid='000000000000000000000001', domain='LightDB', code='light', param={'data': {}})
        self.board = {
            'class': 'test',
            'sorts': [
                {
                    'index': 0,
                    'key': 'schema',
                    'order': 'asc'
                },
                {
                    'index': 1,
                    'key': 'api',
                    'order': 'asc'
                }
            ]
        }

        # self.data = Data(self.board)
