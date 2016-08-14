import unittest

from light.mongo.type import ObjectID, Number
from bson import ObjectId


class TestType(unittest.TestCase):
    def test_parse_object(self):
        result = ObjectID.parse(None)
        self.assertIsNone(result)

        result = ObjectID.parse('000000000000000000000001')
        self.assertEqual(result, ObjectId('000000000000000000000001'))

        result = ObjectID.parse(['000000000000000000000002', '000000000000000000000003'])
        self.assertEqual(result[0], ObjectId('000000000000000000000002'))
        self.assertEqual(result[1], ObjectId('000000000000000000000003'))

        result = ObjectID.parse(ObjectId('000000000000000000000004'))
        self.assertEqual(result, ObjectId('000000000000000000000004'))

    def test_parse_number(self):
        result = Number.parse(None)
        self.assertIsNone(result)

        result = Number.parse(1)
        self.assertEqual(result, 1)

        result = Number.parse([2.0, 3.01, '4', '5.0'])
        self.assertEqual(result[0], 2.0)
        self.assertEqual(result[1], 3.01)
        self.assertEqual(result[2], 4)
        self.assertEqual(result[3], 5.0)
