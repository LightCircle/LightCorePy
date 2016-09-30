import unittest
import json

from light.validate.validator import Validator
from light.http.context import Context
from light.validate.define import Items
from datetime import datetime


class TestValidator(unittest.TestCase):
    def test_is_valid(self):
        self.handler.params.data['age'] = '1'
        result = self.validator.is_valid(['a1'], Items(self.validation))
        print(result)

        self.handler.params.data['date'] = '2000/01/01'
        result = self.validator.is_valid(['b'], Items(self.validation))
        print(result)

        self.handler.params.data['date'] = datetime(2000, 1, 1, 0, 0)
        result = self.validator.is_valid(['b'], Items(self.validation))
        print(result)

        self.handler.params.data['list'] = '4'
        result = self.validator.is_valid(['c'], Items(self.validation))
        print(result)

        self.handler.params.data['password'] = '123'
        result = self.validator.is_valid(['be49d0f4'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = 'something@@somewhere.com'
        result = self.validator.is_valid(['d'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = 'abc@@'
        result = self.validator.is_valid(['d'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = 'abc @.com'
        result = self.validator.is_valid(['d'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = 'email@127.0.0.1'
        result = self.validator.is_valid(['d'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = 'example@inv-.alid-.com'
        result = self.validator.is_valid(['d'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = '"\\\011"@here.com'
        result = self.validator.is_valid(['d'], Items(self.validation))
        print(result)

        self.handler.params.data['url'] = 'http://www.foo.bar/'
        result = self.validator.is_valid(['e'], Items(self.validation))
        print(result)

        self.handler.params.data['url'] = 'http://.www.foo.bar/'
        result = self.validator.is_valid(['e'], Items(self.validation))
        print(result)

        self.handler.params.data['url'] = 'http://##/'
        result = self.validator.is_valid(['e'], Items(self.validation))
        print(result)

        self.handler.params.data['url'] = 'http://a.b--c.de/'
        result = self.validator.is_valid(['e'], Items(self.validation))
        print(result)

        self.handler.params.data['url'] = 'http://10.0.0.1'
        result = self.validator.is_valid(['e'], Items(self.validation))
        print(result)

        self.handler.params.data['ip'] = '123.5.77.88'
        result = self.validator.is_valid(['f'], Items(self.validation))
        print(result)

        self.handler.params.data['ip'] = '900.200.100.75'
        result = self.validator.is_valid(['f'], Items(self.validation))
        print(result)

        self.handler.params.data['ip'] = '127.0.0.abc'
        result = self.validator.is_valid(['f'], Items(self.validation))
        print(result)

        self.handler.params.data['ip'] = 'abcd:ef::42:1'
        result = self.validator.is_valid(['f'], Items(self.validation))
        print(result)

        self.handler.params.data['ip'] = 'abcd:1234::123::1'
        result = self.validator.is_valid(['f'], Items(self.validation))
        print(result)

        self.handler.params.data['json'] = json.dumps({'item1': 1, 'bitem2': 2})
        result = self.validator.is_valid(['h'], Items(self.validation))
        print(result)

        self.handler.params.data['json'] = str({'item1': 1, 'bitem2': 2})
        result = self.validator.is_valid(['h'], Items(self.validation))
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
                'message': 'number not correct'
            },
            {
                'group': 'date_test',
                'name': 'b',
                'rule': 'is_date',
                'key': 'data.date',
                'message': 'date not correct'
            },
            {
                'group': 'dcontains_test',
                'name': 'c',
                'rule': 'contains',
                'key': 'data.list',
                'option': ['1', '2', '3'],
                'message': '[\'1\', \'2\', \'3\'] not contains'
            },
            {
                'group': 'email_test',
                'name': 'd',
                'rule': 'is_email',
                'key': 'data.email',
                'message': 'email not correct'
            },
            {
                'group': 'url_test',
                'name': 'e',
                'rule': 'is_url',
                'key': 'data.url',
                'message': 'url not correct'
            },
            {
                'group': 'ip_test',
                'name': 'f',
                'rule': 'is_ip',
                'key': 'data.ip',
                'option': '4',
                'message': 'ip not correct'
            },
            {
                'group': 'json_test',
                'name': 'h',
                'rule': 'is_json',
                'key': 'data.json',
                'message': 'json not correct'
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
