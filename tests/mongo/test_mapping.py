import unittest

from light.mongo.mapping import Mapping, Items, Item
from bson import ObjectId


class TestMapping(unittest.TestCase):
    def test_parse_data(self):
        # test objectid
        data = {'_id': '000000000000000000000001'}
        Mapping.parse_data(data, Items('items', self.define))
        self.assertEqual(data['_id'], ObjectId('000000000000000000000001'))

        # test number
        data = {'valid': '1'}
        Mapping.parse_data(data, Items('items', self.define))
        self.assertEqual(data['valid'], 1)

        # test key operator
        data = {'$set': {'schema': 1}}
        Mapping.parse_data(data, Items('items', self.define))
        self.assertEqual(data['$set']['schema'], '1')

        # test val operator

    def test_parse_query(self):
        query = {}
        Mapping().parse_query(query, Items('items', self.define))

    def test_default_item(self):
        define = Items('items', self.define)
        self.assertEqual(define.items['_id'].name, 'ID')

    def setUp(self):
        self.define = {
            "_id": {
                "reserved": 1,
                "type": "ObjectID",
                "name": "ID"
            },
            "valid": {
                "reserved": 1,
                "type": "Number",
                "name": "有效标识",
                "description": "1:有效 0:无效"
            },
            "createAt": {
                "reserved": 1,
                "type": "Date",
                "name": "创建时间"
            },
            "createBy": {
                "reserved": 1,
                "type": "String",
                "name": "创建者"
            },
            "schema": {
                "type": "String",
                "name": "Schema名",
                "default": "",
                "description": "",
                "reserved": 2
            },
            "filters": {
                "contents": {
                    "key": {
                        "type": "String",
                        "name": "字段",
                        "default": "",
                        "description": "",
                        "reserved": 2
                    },
                    "operator": {
                        "type": "String",
                        "name": "比较",
                        "default": "$eq",
                        "description": "$eq, $ne, $gt, $gte, $lt, $lte, $in, $nin",
                        "reserved": 2
                    }
                },
                "type": "Array",
                "name": "条件",
                "default": "",
                "description": "",
                "reserved": 2
            },
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
                        "reserved": 2
                    }
                },
                "type": "Array",
                "name": "选择字段",
                "default": "",
                "description": "",
                "reserved": 2
            }
        }
