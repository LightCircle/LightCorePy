import unittest
import re
from datetime import datetime, date

from light.mongo.type import ObjectID, Number, String, Date, Boolean
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

        result = ObjectID.parse({'item0': '000000000000000000000002', 'item1': '000000000000000000000003'})
        self.assertEqual(result['item0'], ObjectId('000000000000000000000002'))
        self.assertEqual(result['item1'], ObjectId('000000000000000000000003'))

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

        result = Number.parse({0: 1, 1: '2', 2: 3.5, 3: '4.2'})
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 2)
        self.assertEqual(result[2], 3.5)
        self.assertEqual(result[3], 4.2)

    def test_parse_string(self):
        result = String.parse(None)
        self.assertEqual(result, '')

        result = String.parse(re.compile('\d+'))
        self.assertEqual(result, re.compile('\d+'))

        result = String.parse([2.0, 's', True, (1, 2, 3)])
        self.assertEqual(result[0], '2.0')
        self.assertEqual(result[1], 's')
        self.assertEqual(result[2], 'True')
        self.assertEqual(result[3], '(1, 2, 3)')

        result = String.parse({'item0': 2.0, 'item1': True, 'item2': (1, 2, 3)})
        self.assertEqual(result['item0'], '2.0')
        self.assertEqual(result['item1'], 'True')
        self.assertEqual(result['item2'], '(1, 2, 3)')

    def test_parse_date(self):
        result = Date.parse(None)
        self.assertIsNone(result)

        result = Date.parse('2008-10-1')
        self.assertEqual(result, datetime(2008, 10, 1))

        result = Date.parse('2008/10/1')
        self.assertEqual(result, datetime(2008, 10, 1))

        result = Date.parse(datetime(2008, 10, 1))
        self.assertEqual(result, datetime(2008, 10, 1))

        result = Date.parse(date(2008, 10, 1))
        self.assertEqual(result, date(2008, 10, 1))

        result = Date.parse([date(2008, 10, 1), datetime(2009, 10, 1), '2010-10-1', '2011/10/1'])
        self.assertEqual(result[0], date(2008, 10, 1))
        self.assertEqual(result[1], datetime(2009, 10, 1))
        self.assertEqual(result[2], datetime(2010, 10, 1))
        self.assertEqual(result[3], datetime(2011, 10, 1))

        result = Date.parse({'item0': '2010-10-1', 'item1': '2011/10/1'})
        self.assertEqual(result['item0'], datetime(2010, 10, 1))
        self.assertEqual(result['item1'], datetime(2011, 10, 1))

    def test_parse_boolean(self):
        result = Boolean.parse(None)
        self.assertEqual(result, False)

        result = Boolean.parse(False)
        self.assertEqual(result, False)
        result = Boolean.parse(True)
        self.assertEqual(result, True)

        result = Boolean.parse('')
        self.assertEqual(result, False)
        result = Boolean.parse('')
        self.assertEqual(result, False)
        result = Boolean.parse('FALSE')
        self.assertEqual(result, False)
        result = Boolean.parse('False')
        self.assertEqual(result, False)
        result = Boolean.parse('0')
        self.assertEqual(result, False)
        result = Boolean.parse('TRUE')
        self.assertEqual(result, True)
        result = Boolean.parse('True')
        self.assertEqual(result, True)
        result = Boolean.parse('bool')
        self.assertEqual(result, True)

        result = Boolean.parse(1)
        self.assertEqual(result, True)
        result = Boolean.parse(0)
        self.assertEqual(result, False)

        result = Boolean.parse(['', 'false', 'true', 0, 1])
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
        self.assertEqual(result[3], False)
        self.assertEqual(result[4], True)

        result = Boolean.parse({'item0': 'false', 'item1': 1})
        self.assertEqual(result['item0'], False)
        self.assertEqual(result['item1'], True)
