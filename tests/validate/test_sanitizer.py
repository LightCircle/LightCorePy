import os
import unittest

from light.validate.sanitizer import Sanitizer
from light.http.context import Context
from light.validate.define import Items
from light.constant import Const

CONST = Const()


class TestSanitizer(unittest.TestCase):
    def test_is_valid(self):
        self.handler.params.data['age'] = '-123.456'
        result = self.sanitizer.to_valid(['a'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['age'] = '-1.e-1'
        result = self.sanitizer.to_valid(['a'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['age'] = '-.123e-1'
        result = self.sanitizer.to_valid(['a'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['age'] = '-123'
        result = self.sanitizer.to_valid(['a'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['date'] = '2001~01~01'
        result = self.sanitizer.to_valid(['b'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['date'] = '2001/01-01'
        result = self.sanitizer.to_valid(['b'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['date'] = '2001.01,01'
        result = self.sanitizer.to_valid(['b'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['ltrim'] = '  \r\n\tfoo  \r\n\t   '
        result = self.sanitizer.to_valid(['cl'], Items(self.sanitization))
        print(result, ':', len(result))

        self.handler.params.data['rtrim'] = '  \r\n\tfoo  \r\n\t   '
        result = self.sanitizer.to_valid(['cr'], Items(self.sanitization))
        print(result, ':', len(result))

        self.handler.params.data['trim'] = '  \r\n\tfoo  \r\n\t   '
        result = self.sanitizer.to_valid(['c'], Items(self.sanitization))
        print(result, ':', len(result))

        self.handler.params.data['escape'] = '<script> alert("xss&fun"); </script>'
        result = self.sanitizer.to_valid(['d'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['escape'] = "<script> alert('xss&fun'); </script>"
        result = self.sanitizer.to_valid(['d'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['escape'] = 'Backtick: `'
        result = self.sanitizer.to_valid(['d'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['unescape'] = '&lt;script&gt; alert(&quot;xss&amp;fun&quot;); &lt;&#x2F;script&gt;'
        result = self.sanitizer.to_valid(['e'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['unescape'] = '&lt;script&gt; alert(&#x27;xss&amp;fun&#x27;); &lt;&#x2F;script&gt;'
        result = self.sanitizer.to_valid(['e'], Items(self.sanitization))
        print(result, ':', type(result))

        self.handler.params.data['unescape'] = 'Backtick: &#96;'
        result = self.sanitizer.to_valid(['e'], Items(self.sanitization))
        print(result, ':', type(result))

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
            },
            {
                'group': 'to_date_test',
                'name': 'b',
                'rule': 'to_date',
                'key': 'data.date',
                'message': 'input date error',
                'option': []
            },
            {
                'group': 'to_ltrim_test',
                'name': 'cl',
                'rule': 'ltrim',
                'key': 'data.ltrim',
                'message': 'input ltrim error',
                'option': []
            },
            {
                'group': 'to_rtrim_test',
                'name': 'cr',
                'rule': 'rtrim',
                'key': 'data.rtrim',
                'message': 'input rtrim error',
                'option': []
            },
            {
                'group': 'to_trim_test',
                'name': 'c',
                'rule': 'trim',
                'key': 'data.trim',
                'message': 'input trim error',
                'option': []
            },
            {
                'group': 'to_escape_test',
                'name': 'd',
                'rule': 'escape',
                'key': 'data.escape',
                'message': 'input escape error',
                'option': []
            },
            {
                'group': 'to_unescape_test',
                'name': 'e',
                'rule': 'unescape',
                'key': 'data.unescape',
                'message': 'input unescape error',
                'option': []
            }
        ]
