import os
import unittest

from light.validator import Validator
from light.http.context import Context
from light.constant import Const

CONST = Const()


class TestValidator(unittest.TestCase):
    def test_is_valid(self):
        self.handler.params.data['age'] = '1'
        result = self.validator.is_valid(['a1'], self.validation)
        print(result)

        result = self.validator.is_valid(['be49d0f4'], self.validation)
        print(result)

    def setUp(self):

        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'db.alphabets.cn'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        self.handler = Context(uid='000000000000000000000001', domain='LightDB', code='light', param={'data': {}})
        self.validator = Validator(self.handler)
        self.validation = [
            {
                'group': 'number_test',
                'name': 'a1',
                'rule': 'is_number',
                'key': 'data.age',
                'message': 'a1 not correct',
                'option': []
            },
            {
                'group': 'unique_test',
                'name': 'be49d0f4',
                'rule': 'is_unique',
                'key': 'data.id',
                'option': {
                    'table': 'user',
                    'condition': {
                        'id': 'sloan'
                    }
                },
                'message': '用户名已经存在'
            }
        ]
