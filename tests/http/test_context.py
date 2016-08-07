import unittest

from light.http.context import Params


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
