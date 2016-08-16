import unittest

from light.mongo.mapping import Update, Items, Item
from bson import ObjectId


class TestMapping(unittest.TestCase):
    def test_parse_data(self):
        # test objectid
        data = {'_id': '000000000000000000000001'}
        Update.parse(data, Items('items', self.define))
        self.assertEqual(data['_id'], ObjectId('000000000000000000000001'))

        # # test number
        # data = {'valid': '1'}
        # Update.parse_data(data, Items('items', self.define))
        # self.assertEqual(data['valid'], 1)
        #
        # # test key operator
        # data = {'$set': {'schema': 1}}
        # Update.parse_data(data, Items('items', self.define))
        # self.assertEqual(data['$set']['schema'], '1')
        #
        # # test key operator
        # data = {'$inc': {'item1': '1', 'item2': '2'}}
        # Update.parse_data(data, Items('items', self.define))
        # self.assertEqual(data['$inc']['item1'], 1)
        # self.assertEqual(data['$inc']['item2'], 2)

        # test val operator
        # data = {'$push': {'fields': {'$each': [1, 2, 3]}}}
        # Update.parse_data(data, Items('items', self.define))
        # self.assertEqual(data['$push']['fields']['$each'], ['1', '2', '3'])

        # # test array value
        # data = {'$push': {'fields': [1, 2, 3]}}
        # Update.parse_data(data, Items('items', self.define))
        # self.assertEqual(data['$push']['fields'], ['1', '2', '3'])
        #
        # data = {'selects': [{'select': 0, 'fields': 1}, {'select': 1, 'fields': 2}]}
        # Update.parse_data(data, Items('items', self.define))
        # self.assertEqual(data['$push']['fields'], ['1', '2', '3'])

    def test_parse_query(self):
        query = {}
        # Update().parse_query(query, Items('items', self.define))

    def test_default_item(self):
        define = Items('items', self.define)
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
