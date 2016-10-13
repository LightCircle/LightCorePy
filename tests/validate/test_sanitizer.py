import os
import unittest

from light.validate.sanitizer import Sanitizer
from light.http.context import Context
from light.validate.define import Items
from light.constant import Const

CONST = Const()


class TestSanitizer(unittest.TestCase):
    def test_is_valid(self):
        self.handler.params.data['age'] = '1.1'
        result = self.sanitizer.to_valid(['a'], Items(self.sanitization))
        if result is True:
            print(self.handler.params.data['age'])
        else:
            print(result)

    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'localhost'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '27017'
        # os.environ[CONST.ENV_LIGHT_DB_HOST] = 'db.alphabets.cn'
        # os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        # os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        # os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        self.handler = Context(uid='000000000000000000000001', domain='LightDBII', code='light', param={'data': {}})
        self.sanitizer = Sanitizer(self.handler)
        self.sanitization = [
            {
                'group': 'to_number_test',
                'name': 'a',
                'rule': 'to_number',
                'key': 'data.age',
                'message': 'input number error',
                'option': []
            }
        ]
