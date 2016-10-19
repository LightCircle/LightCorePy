import os
import unittest
import json

from datetime import datetime
from light.validate.validator import Validator
from light.http.context import Context
from light.validate.define import Items
from light.constant import Const

CONST = Const()


class TestValidator(unittest.TestCase):
    def test_is_valid(self):
        self.handler.params.data['age'] = '  1  '
        result = self.validator.is_valid(['a1'], Items(self.validation))
        print(result)

        self.handler.params.data['age'] = '-.123e-1'
        result = self.validator.is_valid(['a1'], Items(self.validation))
        print(result)

        self.handler.params.data['age'] = '-12.345'
        result = self.validator.is_valid(['a1'], Items(self.validation))
        print(result)

        self.handler.params.data['date'] = '2000/01/01'
        result = self.validator.is_valid(['b'], Items(self.validation))
        print(result)

        self.handler.params.data['date'] = '2000-01-01'
        result = self.validator.is_valid(['b'], Items(self.validation))
        print(result)

        self.handler.params.data['date'] = datetime(2000, 1, 1, 0, 0)
        result = self.validator.is_valid(['b'], Items(self.validation))
        print(result)

        self.handler.params.data['boolean'] = 'abc'
        result = self.validator.is_valid(['bt'], Items(self.validation))
        print(result)

        self.handler.params.data['boolean'] = 'true'
        result = self.validator.is_valid(['bt'], Items(self.validation))
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

        self.handler.params.data['email'] = ['h.luo@alphabets.cn', 'h.shen@alphabets.cn']
        result = self.validator.is_valid(['cd49d0f4'], Items(self.validation))
        print(result)

        self.handler.params.data['email'] = 'h.shen@alphabets.cn'
        result = self.validator.is_valid(['af49d0f4'], Items(self.validation))
        print(result)

        self.handler.params.data['id'] = {}
        result = self.validator.is_valid(['zx49d0f4'], Items(self.validation))
        print(result)

        self.handler.params.data['id'] = '  \t\n  '
        result = self.validator.is_valid(['zx49d0f4'], Items(self.validation))
        print(result)

        self.handler.params.data['id'] = '-NaN'
        result = self.validator.is_valid(['zx49d0f4'], Items(self.validation))
        print(result)

        self.handler.params.data['id'] = '  1   '
        result = self.validator.is_valid(['zx49d0f4'], Items(self.validation))
        print(result)

    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'localhost'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '27017'
        # os.environ[CONST.ENV_LIGHT_DB_HOST] = 'db.alphabets.cn'
        # os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        # os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        # os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

        self.handler = Context(uid='000000000000000000000001', domain='LightDBII', code='light', param={'data': {}})
        self.validator = Validator(self.handler)
        self.validation = [
            {
                'group': 'number_test',
                'name': 'a1',
                'rule': 'is_number',
                'prerule': ['to_number', 'trim'],
                'key': 'data.age',
                'message': 'number not correct',
                'option': []
            },
            {
                'group': 'date_test',
                'name': 'b',
                'rule': 'is_date',
                'prerule': ['to_date'],
                'key': 'data.date',
                'message': 'date not correct',
                'option': []
            },
            {
                'group': 'boolean_test',
                'name': 'bt',
                'rule': 'is_boolean',
                'prerule': ['to_boolean'],
                'key': 'data.boolean',
                'message': 'boolean not correct',
                'option': []
            },
            {
                'group': 'contains_test',
                'name': 'c',
                'rule': 'contains',
                'prerule': [],
                'key': 'data.list',
                'option': ['1', '2', '3'],
                'message': '[\'1\', \'2\', \'3\'] not contains',
            },
            {
                'group': 'email_test',
                'name': 'd',
                'rule': 'is_email',
                'prerule': [],
                'key': 'data.email',
                'message': 'email not correct',
                'option': []
            },
            {
                'group': 'url_test',
                'name': 'e',
                'rule': 'is_url',
                'prerule': [],
                'key': 'data.url',
                'message': 'url not correct',
                'option': []
            },
            {
                'group': 'ip_test',
                'name': 'f',
                'rule': 'is_ip',
                'prerule': [],
                'key': 'data.ip',
                'option': '4',
                'message': 'ip not correct'
            },
            {
                'group': 'json_test',
                'name': 'h',
                'rule': 'is_json',
                'prerule': [],
                'key': 'data.json',
                'message': 'json not correct',
                'option': []
            },
            {
                'group': '/api/access/add',
                'name': 'be49d0f4',
                'rule': 'range',
                'prerule': [],
                'key': 'data.password',
                'option': ['4', '16'],
                'message': '密码长度需要在4-16位'
            },
            {
                'group': 'exists_test',
                'name': 'cd49d0f4',
                'rule': 'is_exists',
                'prerule': [],
                'key': 'data.id',
                'option': {
                    'table': 'user',
                    'condition': {
                        'id': {'$in': ['shen', 'luohao']},
                        'email': '$data.email'
                    }
                },
                'message': '值不存在表里'
            },
            {
                'group': 'unique_test',
                'name': 'af49d0f4',
                'rule': 'is_unique',
                'prerule': [],
                'key': 'data.id',
                'option': {
                    'table': 'user',
                    'condition': {
                        'id': 'shen',
                        'email': '$data.email'
                    }
                },
                'message': '用户名已经存在'
            },
            {
                'group': 'required_test',
                'name': 'zx49d0f4',
                'rule': 'is_required',
                'prerule': [],
                'key': 'data.id',
                'option': '',
                'message': '这是必填字段'
            }
        ]
