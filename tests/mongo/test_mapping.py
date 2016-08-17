import unittest

from light.mongo.mapping import Update, Query
from light.mongo.define import Items
from datetime import datetime, date
from bson import ObjectId


class TestMapping(unittest.TestCase):
    def test_parse_data(self):
        """
        test type convert
        """

        # test basic data type
        data = {'_id': '000000000000000000000001'}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['_id'], ObjectId('000000000000000000000001'))

        # test number
        data = {'valid': '1'}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['valid'], 1)

        """
        test mongodb operator
        """

        # $inc
        data = {'$inc': {'item1': '1', 'item2': '2'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$inc']['item1'], 1)
        self.assertEqual(data['$inc']['item2'], 2)

        # $set
        data = {'$set': {'schema': 1}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$set']['schema'], '1')

        # $push
        data = {'$push': {'fields': 2}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$push']['fields'], '2')

        # $push $each
        data = {'$push': {'fields': {'$each': [1, 2, 3]}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$push']['fields']['$each'], ['1', '2', '3'])

        # $push $slice
        data = {'$push': {'fields': {'$slice': '2'}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$push']['fields']['$slice'], 2)

        # $push $sort
        data = {'$push': {'fields': {'$sort': '-1'}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$push']['fields']['$sort'], -1)

        # $push $position
        data = {'$push': {'fields': {'$position': '1'}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$push']['fields']['$position'], 1)

        """
        test sub document
        """

        # array
        data = {'selects': [{'select': 0, 'fields': [1, 2]}, {'select': 1}]}
        Update.parse(data, Items(self.define))
        self.assertFalse(data['selects'][0]['select'])
        self.assertTrue(data['selects'][1]['select'])

        # object
        data = {'limit': {'date': '2006/01/01', 'count': '1'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['limit'], {'date': datetime(2006, 1, 1, 0, 0), 'count': 1})

    def test_parse_query(self):
        """
        test basic type
        """
        query = {'_id': '000000000000000000000001', 'valid': '1', 'createAt': '2016/01/01', 'schema': 2}
        Query.parse(query, Items(self.define))
        self.assertEqual(query, {
            '_id': ObjectId('000000000000000000000001'),
            'valid': 1,
            'createAt': datetime(2016, 1, 1, 0, 0),
            'schema': '2'
        })

        """
        test mongodb operator : comparison
        """
        # $eq
        query = {'valid': {'$eq': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$eq'], 1)

        # $eq top level
        query = {'$eq': {'valid': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$eq']['valid'], 1)

        # $gt
        query = {'valid': {'$gt': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$gt'], 1)

        """
        test mongodb operator : logical
        """
        # $or
        query = {'$or': [{'valid': '1'}, {'valid': '2'}]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$or'][0]['valid'], 1)
        self.assertEqual(query['$or'][1]['valid'], 2)

        # $or $gt $lt $in
        query = {'$or': [
            {'valid': {'$gt': '1'}},
            {'valid': {'$lt': '2'}},
            {'valid': {'$in': ['1', '2']}}
        ]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$or'][0]['valid'], {'$gt': 1})
        self.assertEqual(query['$or'][1]['valid'], {'$lt': 2})
        self.assertEqual(query['$or'][2]['valid']['$in'], [1, 2])

        # $and $gt $lt $in
        query = {'$and': [
            {'valid': {'$gt': '1'}},
            {'valid': {'$lt': '2'}},
            {'valid': {'$in': ['1', '2']}}
        ]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$and'][0]['valid'], {'$gt': 1})
        self.assertEqual(query['$and'][1]['valid'], {'$lt': 2})
        self.assertEqual(query['$and'][2]['valid']['$in'], [1, 2])

        # $and + $or
        query = {'$and': [
            {'$or': [{'valid': {'$gt': '10'}}, {'valid': {'$lt': '12'}}]},
            {'$or': [{'valid': {'$gt': '15'}}, {'valid': {'$lt': '17'}}]}
        ]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$and'][0]['$or'][0]['valid'], {'$gt': 10})
        self.assertEqual(query['$and'][1]['$or'][1]['valid'], {'$lt': 17})

    def test_default_item(self):
        define = Items(self.define)
        self.assertEqual(define.items['_id'].name, 'ID')

    def setUp(self):
        self.define = {
            # ObjectID type
            "_id": {
                "reserved": 1,
                "type": "ObjectID",
                "name": "ID"
            },
            # Number type
            "valid": {
                "reserved": 1,
                "type": "Number",
                "name": "有效标识",
                "description": "1:有效 0:无效"
            },
            # Date type
            "createAt": {
                "reserved": 1,
                "type": "Date",
                "name": "创建时间"
            },
            # String type
            "schema": {
                "type": "String",
                "name": "Schema名",
                "default": "",
                "description": "",
                "reserved": 2
            },
            # Array basic type
            "fields": {
                "type": "Array",
                "name": "附加项 关联后选择的字段",
                "default": "",
                "description": "",
                "reserved": 2,
                "contents": "String"
            },
            # Array type
            "selects": {
                "contents": {
                    "select": {
                        "type": "Boolean",
                        "name": "选中",
                        "default": "false",
                        "description": "",
                        "reserved": 2
                    },
                    "fields": {
                        "type": "Array",
                        "name": "附加项 关联后选择的字段",
                        "default": "",
                        "description": "",
                        "reserved": 2,
                        "contents": "String"
                    }
                },
                "type": "Array",
                "name": "选择字段",
                "default": "",
                "description": "",
                "reserved": 2
            },
            # Object type
            "limit": {
                "contents": {
                    "date": {
                        "type": "Date",
                        "name": "备份截止日",
                        "default": "",
                        "description": "",
                        "reserved": 2
                    },
                    "count": {
                        "type": "Number",
                        "name": "备份次数",
                        "default": "",
                        "description": "",
                        "reserved": 2
                    }
                },
                "type": "Object",
                "name": "限制",
                "default": "",
                "description": "",
                "reserved": 2
            }
        }
