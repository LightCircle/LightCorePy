import unittest

from light.validator import Validator
from light.http.context import Context


class TestValidator(unittest.TestCase):
    def test_is_valid(self):
        self.handler.params.data['age'] = '1'
        result = self.validator.is_valid(['a1'], self.validation)
        print(result)

        # self.assertTrue(validator.is_number(1))
        # self.assertFalse(validator.is_number('1'))
        # self.assertTrue(validator.is_number(1.0))
        # self.assertFalse(validator.is_number(None))
        # self.assertFalse(validator.is_number(True))

    def setUp(self):
        self.handler = Context(uid='000000000000000000000001', domain='LightDB', code='light', param={'data': {}})
        self.validator = Validator(self.handler)
        self.validation = [
            {
                'group': 'number_test',
                'name': 'a1',
                'rule': 'is_number',
                'key': 'data.age',
                'message': 'a1 not correct'
            },
            {
                'group': '/api/access/add',
                'name': 'be49d0f4',
                'rule': 'range',
                'key': 'data.password',
                'option': ['4', '16'],
                'message': '密码长度需要在4-16位'
            },
            {
                'group': '',
                'name': 'staff_check_10',
                'rule': 'exists',
                'key': 'data.project',
                'option': {
                    'table': 'group',
                    'conditions': {
                        '_id': '$data.project'
                    }
                }
            }
        ]
