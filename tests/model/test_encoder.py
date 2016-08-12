import json
import unittest

from light.mongo.encoder import JsonEncoder
from bson import ObjectId
from datetime import datetime


class TestEncoder(unittest.TestCase):
    def test_init(self):
        data = {'_id': ObjectId('000000000000000000000001'), 'date': datetime(2015, 7, 1, 4, 54, 9, 344000)}
        self.assertEqual('{"date": "2015-07-01T04:54:09.344000Z", "_id": "000000000000000000000001"}',
                         json.dumps(data, cls=JsonEncoder))
