import unittest

from light.http.context import Params, Context


class TestParams(unittest.TestCase):
    def setUp(self):
        self.params = Params({
            'a': 'a',
            'condition': {
                'b': 10
            }
        })

    def test_getter(self):
        self.assertEqual(self.params.condition['b'], 10)
        self.assertEqual(self.params.a, 'a')


class TestContext(unittest.TestCase):
    def setUp(self):
        pass

    def test_by_manually(self):
        handler = Context('1', 'LightDB', 'light', {})

        self.assertEqual(handler.uid, '1')
        self.assertEqual(handler.domain, 'LightDB')
        self.assertEqual(handler.code, 'light')

        handler.add_params('id', '1')
        self.assertEqual(handler.params.id, '1')

        handler.extend_params({'key': '2'})
        self.assertEqual(handler.params.id, '1')
        self.assertEqual(handler.params.key, '2')

        handler.remove_params('key')
        self.assertEqual(handler.params.id, '1')
        self.assertIsNone(handler.params.key)
