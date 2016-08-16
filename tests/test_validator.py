import unittest

from light import validator


class TestValidator(unittest.TestCase):
    def test_is_number(self):

        self.assertTrue(validator.is_number(1))
        self.assertFalse(validator.is_number('1'))
        self.assertTrue(validator.is_number(1.0))
        self.assertFalse(validator.is_number(None))
        self.assertFalse(validator.is_number(True))

    def test_is_string(self):
        self.assertFalse(validator.is_string(1))
        self.assertTrue(validator.is_string("1"))
        self.assertFalse(validator.is_string(['1', '2', '3']))
