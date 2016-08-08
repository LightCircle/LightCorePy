import unittest
import light.helper


class TestHelper(unittest.TestCase):
    def setUp(self):
        pass

    def test_resolve(self):
        empty= light.helper.resolve('empty')
        self.assertIsNone(empty)
