import unittest
import re

from light.mongo.mapping import Update, Query
from light.mongo.define import Items
from datetime import datetime
from bson import ObjectId


class TestMapping(unittest.TestCase):
    def test_parse_data(self):
        """
        test type convert
        """
        # 'None' type
        data = {None: None}
        Update.parse(data, Items(self.define))
        self.assertEqual(data[None], None)

        # data = None
        data = None
        Update.parse(data, Items(self.define))
        self.assertEqual(data, None)

        # test basic data type
        data = {'_id': '000000000000000000000001'}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['_id'], ObjectId('000000000000000000000001'))

        # test number
        data = {'valid': '1'}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['valid'], 1)

        data = {'fields': ['1', '2', '3']}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['fields'], ['1', '2', '3'])

        data = {'valid': 1, 'createAt': {'$gt': datetime(1900, 1, 1, 0, 0)}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['valid'], 1)
        self.assertEqual(data['createAt']['$gt'], datetime(1900, 1, 1, 0, 0))

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

        """

        test mongodb operator

        """

        """
        Field Update Operators
        """

        # $inc
        data = {'$inc': {'item1': '1', 'item2': '2'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$inc']['item1'], 1)
        self.assertEqual(data['$inc']['item2'], 2)

        # $mul
        data = {'$mul': {'item1': '10.1'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$mul']['item1'], 10.1)

        # $rename
        data = {'$rename': {'item1': 'name'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$rename']['item1'], 'name')

        # $setOnInsert
        data = {'$setOnInsert': {'schema': 1}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$setOnInsert']['schema'], '1')

        data = {'$setOnInsert': {'nestsii.fields.nestarray.0.date': '2001/01/01'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$setOnInsert']['nestsii.fields.nestarray.0.date'], datetime(2001, 1, 1, 0, 0))

        # $set
        data = {'$set': {'schema': 1}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$set']['schema'], '1')

        data = {'$set': {'nests': [{'select': 0, 'fields': [{'nestins': 2}, {'nestins': 3}]}, {'select': 1}]}}
        Update.parse(data, Items(self.define))
        self.assertFalse(data['$set']['nests'][0]['select'])
        self.assertTrue(data['$set']['nests'][1]['select'])
        self.assertEqual(data['$set']['nests'][0]['fields'][0]['nestins'], '2')

        data = {'$set': {'selects': [{'select': 0, 'fields': [1, 2]}, {'select': 1}]}}
        Update.parse(data, Items(self.define))
        self.assertFalse(data['$set']['selects'][0]['select'])
        self.assertTrue(data['$set']['selects'][1]['select'])

        data = {'$set': {'limit': {'date': '2006/01/01', 'count': '1'}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$set']['limit'], {'date': datetime(2006, 1, 1, 0, 0), 'count': 1})

        # $unset
        data = {'$unset': {'schema': 1, 'valid': '2'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$unset']['schema'], '')
        self.assertEqual(data['$unset']['valid'], '')

        # $min
        data = {'$min': {'createAt': '2006/01/01', 'valid': '2'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$min']['createAt'], datetime(2006, 1, 1, 0, 0))
        self.assertEqual(data['$min']['valid'], 2)

        # $max
        data = {'$max': {'createAt': '2006/01/01', 'valid': '2'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$max']['createAt'], datetime(2006, 1, 1, 0, 0))
        self.assertEqual(data['$max']['valid'], 2)

        # $currentDate
        data = {'$currentDate': {'createAt': 'true', 'cancellation.date': {'$type': 'timestamp'}}}
        Update.parse(data, Items(self.define))
        self.assertTrue(data['$currentDate']['createAt'])
        self.assertEqual(data['$currentDate']['cancellation.date']['$type'], 'timestamp')

        """
        Array Update Operators
        """

        # $pop
        data = {'$pop': {'item1': '1'}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pop']['item1'], 1)

        # $addToSet
        data = {'$addToSet': {'fields': 2}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$addToSet']['fields'], '2')

        data = {'$addToSet': {'nests.0.fields.0.nestarray': [2, 3]}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$addToSet']['nests.0.fields.0.nestarray'], ['2', '3'])

        # $addToSet $each
        data = {'$addToSet': {'fields': {'$each': [1, 2, 3]}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$addToSet']['fields']['$each'], ['1', '2', '3'])

        data = {'$addToSet': {'nests.0.fields.0.nestarray': {'$each': [1, 2, 3]}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$addToSet']['nests.0.fields.0.nestarray']['$each'], ['1', '2', '3'])

        #
        data = {'$addToSet': {'nests': {'$each': [
            {'fields': {'valid': '5', 'nestins': 6, 'nestarray': [11, 12, 13]}, 'select': 1},
            {'fields': {'valid': '8', 'nestins': 10}, 'select': 0}
        ]}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$addToSet']['nests']['$each'][0]['fields']['valid'], 5)
        self.assertEqual(data['$addToSet']['nests']['$each'][1]['fields']['nestins'], '10')
        self.assertEqual(data['$addToSet']['nests']['$each'][0]['fields']['nestarray'], ['11', '12', '13'])
        self.assertFalse(data['$addToSet']['nests']['$each'][1]['select'])

        #
        data = {'$addToSet': {'nestsii': {'$each': [
            {'fields': {'nestarray': [{'date': '2000/01/01'}, {'date': '2001/01/01'}]}, 'select': 1},
            {'fields': [{'nestarray': [{'date': '2002/01/01'}, {'date': '2003/01/01'}]},
                        {'nestarray': [{'date': '2004/01/01'}, {'date': '2005/01/01'}]}], 'select': 0}
        ]}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$addToSet']['nestsii']['$each'][0]['fields']['nestarray'][0]['date'],
                         datetime(2000, 1, 1, 0, 0))
        self.assertTrue(data['$addToSet']['nestsii']['$each'][0]['select'])
        self.assertEqual(data['$addToSet']['nestsii']['$each'][1]['fields'][0]['nestarray'][0]['date'],
                         datetime(2002, 1, 1, 0, 0))
        self.assertEqual(data['$addToSet']['nestsii']['$each'][1]['fields'][1]['nestarray'][1]['date'],
                         datetime(2005, 1, 1, 0, 0))
        self.assertFalse(data['$addToSet']['nestsii']['$each'][1]['select'])

        # $pullAll
        data = {'$pullAll': {'fields': [1, 2, 3]}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pullAll']['fields'], ['1', '2', '3'])

        # $pull
        data = {'$pull': {'fields': 1}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pull']['fields'], '1')

        data = {'$pull': {'fields.0': 1}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pull']['fields.0'], '1')

        data = {'$pull': {'fields': {'$in': [1, 2, 3]}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pull']['fields']['$in'], ['1', '2', '3'])

        # $pull + $elemMatch
        data = {'$pull': {'selects': {'$elemMatch': {'select': 0, 'valid': '1'}}}}
        Update.parse(data, Items(self.define))
        self.assertFalse(data['$pull']['selects']['$elemMatch']['select'])
        self.assertEqual(data['$pull']['selects']['$elemMatch']['valid'], 1)

        data = {'$pull': {'nests': {'fields': {'$elemMatch': {'valid': '1', 'nestins': {'$gte': 8}}}}}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pull']['nests']['fields']['$elemMatch']['valid'], 1)
        self.assertEqual(data['$pull']['nests']['fields']['$elemMatch']['nestins']['$gte'], '8')

        # $pushAll
        data = {'$pushAll': {'fields': [1, 2, 3]}}
        Update.parse(data, Items(self.define))
        self.assertEqual(data['$pushAll']['fields'], ['1', '2', '3'])

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
        Bitwise Update Operators
        """

        """
        Isolation Update Operators
        """

    def test_parse_query(self):
        """
        test basic type
        """
        # 'None' type
        query = {None: None}
        Query.parse(query, Items(self.define))
        self.assertEqual(query, {None: None})

        # query = None
        query = None
        Query.parse(query, Items(self.define))
        self.assertEqual(query, None)

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

        query = {'nestsii.fields.nestarray.0.date': {'$eq': '2001/01/01'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['nestsii.fields.nestarray.0.date']['$eq'], datetime(2001, 1, 1, 0, 0))

        query = {'fields': {'$eq': [1, 2, 3]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$eq'], ['1', '2', '3'])

        # $gt
        query = {'valid': {'$gt': '1', '$lt': '2'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$gt'], 1)
        self.assertEqual(query['valid']['$lt'], 2)

        query = {'fields': {'$gt': 8, '$lte': 10}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$gt'], '8')
        self.assertEqual(query['fields']['$lte'], '10')

        # $gte
        query = {'createAt': {'$gte': '2006/01/01'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['createAt']['$gte'], datetime(2006, 1, 1, 0, 0))

        # $lt
        query = {'schema': {'$lt': 1}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['schema']['$lt'], '1')

        # $lte
        query = {'valid': {'$lte': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$lte'], 1)

        # $ne
        query = {'schema': {'$ne': 1}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['schema']['$ne'], '1')

        query = {'fields': {'$ne': 1}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$ne'], '1')

        # $in
        query = {'valid': {'$in': ['1', '2', '3']}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$in'], [1, 2, 3])

        query = {'fields': {'$in': [1, 2, 3]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$in'], ['1', '2', '3'])

        # $nin
        query = {'schema': {'$nin': [1, 2, 3]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['schema']['$nin'], ['1', '2', '3'])

        query = {'fields': {'$nin': [1, 2, 3]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$nin'], ['1', '2', '3'])

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

        # $and
        query = {'$and': [{'valid': '1'}, {'valid': '2'}]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$and'][0]['valid'], 1)
        self.assertEqual(query['$and'][1]['valid'], 2)

        query = {'$and': [{'valid': {'$ne': '1'}}, {'valid': {'$exists': 'false'}}]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$and'][0]['valid']['$ne'], 1)
        self.assertFalse(query['$and'][1]['valid']['$exists'])

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

        # $not
        query = {'valid': {'$not': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$not'], 1)

        query = {'valid': {'$not': {'$gt': '1'}}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$not']['$gt'], 1)

        query = {'valid': {'$not': {'$in': ['1', '2']}}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$not']['$in'], [1, 2])

        # $nor
        query = {'$nor': [
            {'flag': 'true'},
            {'valid': {'$lt': '2'}},
            {'valid': {'$exists': 'false'}}
        ]}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$nor'][0]['flag'], True)
        self.assertEqual(query['$nor'][1]['valid']['$lt'], 2)
        self.assertEqual(query['$nor'][2]['valid']['$exists'], False)

        """
        test mongodb operator : Element
        """
        # $exists
        query = {'flag': {'$exists': 'true'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['flag']['$exists'], True)

        # $type
        query = {'abstract': {'$type': 1}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'double')

        query = {'abstract': {'$type': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'double')

        query = {'abstract': {'$type': 2}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'string')

        query = {'abstract': {'$type': '3'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'object')

        query = {'abstract': {'$type': 4}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'array')

        query = {'abstract': {'$type': '5'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'binData')

        query = {'abstract': {'$type': 6}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'undefined')

        query = {'abstract': {'$type': '7'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'objectId')

        query = {'abstract': {'$type': 8}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'bool')

        query = {'abstract': {'$type': '9'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'date')

        query = {'abstract': {'$type': 10}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'null')

        query = {'abstract': {'$type': '11'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'regex')

        query = {'abstract': {'$type': 12}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'dbPointer')

        query = {'abstract': {'$type': '13'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'javascript')

        query = {'abstract': {'$type': 14}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'symbol')

        query = {'abstract': {'$type': '15'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'javascriptWithScope')

        query = {'abstract': {'$type': 16}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'int')

        query = {'abstract': {'$type': '17'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'timestamp')

        query = {'abstract': {'$type': 18}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'long')

        query = {'abstract': {'$type': '-1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'minKey')

        query = {'abstract': {'$type': -1}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'minKey')

        query = {'abstract': {'$type': '127'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'maxKey')

        query = {'abstract': {'$type': 127}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['abstract']['$type'], 'maxKey')

        """
        test mongodb operator : Evaluation
        """

        # $mod
        query = {'valid': {'$mod': ['2', '0']}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['valid']['$mod'], [2, 0])

        # $regex
        query = {'general': {'$regex': re.compile(r'^S\d+'), '$options': 'm'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['general']['$regex'], re.compile(r'^S\d+'))
        self.assertEqual(query['general']['$options'], 'm')

        # $text
        query = {'$text': {'$search': 'fields', '$caseSensitive': 'true'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['$text']['$search'], 'fields')
        self.assertEqual(query['$text']['$caseSensitive'], True)

        """
        test mongodb operator : Query Array
        """

        # $all
        query = {'schema': {'$all': [1, 2]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['schema']['$all'], ['1', '2'])

        query = {'general': {'$all': [{'valid': {'$lt': '12'}}, [1, 2], '10']}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['general']['$all'][0], {'valid': {'$lt': '12'}})
        self.assertEqual(query['general']['$all'][1], [1, 2])
        self.assertEqual(query['general']['$all'][2], '10')

        query = {'schema': {'$all': [[1, 2], [3, 4]]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['schema']['$all'], [['1', '2'], ['3', '4']])

        query = {'limit': {'$all': [{'date': '2006/01/01', 'count': '1'}]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['limit']['$all'][0]['date'], datetime(2006, 1, 1, 0, 0))
        self.assertEqual(query['limit']['$all'][0]['count'], 1)

        query = {'limit': {'$all': [[{'date': '2006/01/01', 'count': '1'}]]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['limit']['$all'][0][0]['date'], datetime(2006, 1, 1, 0, 0))
        self.assertEqual(query['limit']['$all'][0][0]['count'], 1)

        # $all + $elemMatch
        query = {'limit': {'$all': [{'$elemMatch': {'date': '2006/01/01', 'count': '1'}}]}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['limit']['$all'][0]['$elemMatch']['date'], datetime(2006, 1, 1, 0, 0))
        self.assertEqual(query['limit']['$all'][0]['$elemMatch']['count'], 1)

        # $elemMatch
        query = {'selects': {'$elemMatch': {'fields': {'$gte': 8, '$lt': 10}, 'select': 0}}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['selects']['$elemMatch']['fields']['$gte'], '8')
        self.assertFalse(query['selects']['$elemMatch']['select'])

        query = {
            'nests': {
                '$elemMatch': {
                    'fields': {'valid': {'$gte': '8'}, 'nestarray': {'$gte': 8, '$lt': 10}}, 'select': 0
                }
            }
        }
        Query.parse(query, Items(self.define))
        self.assertEqual(query['nests']['$elemMatch']['fields']['valid']['$gte'], 8)
        self.assertEqual(query['nests']['$elemMatch']['fields']['nestarray']['$gte'], '8')
        self.assertEqual(query['nests']['$elemMatch']['fields']['nestarray']['$lt'], '10')
        self.assertFalse(query['nests']['$elemMatch']['select'])

        query = {'fields': {'$elemMatch': {'$gte': 8, '$lt': 5}}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$elemMatch']['$gte'], '8')
        self.assertEqual(query['fields']['$elemMatch']['$lt'], '5')

        # $size
        query = {'fields': {'$size': '1'}}
        Query.parse(query, Items(self.define))
        self.assertEqual(query['fields']['$size'], 1)

    def test_default_item(self):
        define = Items(self.define)
        self.assertEqual(define.items['_id'].name, 'ID')

    def setUp(self):
        self.define = {
            # ObjectID type
            '_id': {
                'reserved': 1,
                'type': 'ObjectID',
                'name': 'ID'
            },
            # Number type
            'valid': {
                'reserved': 1,
                'type': 'Number',
                'name': '有效标识',
                'description': '1:有效 0:无效'
            },
            # Boolean type
            'flag': {
                'reserved': 1,
                'type': 'Boolean',
                'name': 'Flag'
            },
            # Date type
            'createAt': {
                'reserved': 1,
                'type': 'Date',
                'name': '创建时间'
            },
            # String type
            'schema': {
                'type': 'String',
                'name': 'Schema名',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Array basic type
            'fields': {
                'type': 'Array',
                'name': '附加项 关联后选择的字段',
                'default': '',
                'description': '',
                'reserved': 2,
                'contents': 'String'
            },
            # Array Object type
            'general': {
                'type': 'Array',
                'name': '附加项 关联后选择的字段',
                'default': '',
                'description': '',
                'reserved': 2,
                'contents': 'Object'
            },
            # Object type
            'abstract': {
                'type': 'Object',
                'name': 'Abstract名',
                'default': '',
                'description': '',
                'reserved': 2,
            },
            # Array type
            'selects': {
                'contents': {
                    'select': {
                        'type': 'Boolean',
                        'name': '选中',
                        'default': 'false',
                        'description': '',
                        'reserved': 2
                    },
                    'fields': {
                        'type': 'Array',
                        'name': '附加项 关联后选择的字段',
                        'default': '',
                        'description': '',
                        'reserved': 2,
                        'contents': 'String'
                    },
                    'valid': {
                        'reserved': 1,
                        'type': 'Number',
                        'name': '有效标识',
                        'description': '1:有效 0:无效'
                    }
                },
                'type': 'Array',
                'name': '选择字段',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Array-Nest type
            'nests': {
                'contents': {
                    'select': {
                        'type': 'Boolean',
                        'name': '选中',
                        'default': 'false',
                        'description': '',
                        'reserved': 2
                    },
                    'fields': {
                        'type': 'Array',
                        'name': '附加项 关联后选择的字段',
                        'default': '',
                        'description': '',
                        'reserved': 2,
                        'contents': {
                            'valid': {
                                'reserved': 1,
                                'type': 'Number',
                                'name': '有效标识',
                                'description': '1:有效 0:无效'
                            },
                            'nestins': {
                                'type': 'String',
                                'name': '嵌套',
                                'default': '',
                                'description': '',
                                'reserved': 2
                            },
                            'nestarray': {
                                'type': 'Array',
                                'name': '附加项 关联后选择的字段',
                                'default': '',
                                'description': '',
                                'reserved': 2,
                                'contents': 'String'
                            }
                        }
                    }
                },
                'type': 'Array',
                'name': '选择字段',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Array-Nest-II type
            'nestsii': {
                'contents': {
                    'select': {
                        'type': 'Boolean',
                        'name': '选中',
                        'default': 'false',
                        'description': '',
                        'reserved': 2
                    },
                    'fields': {
                        'type': 'Array',
                        'name': '附加项 关联后选择的字段',
                        'default': '',
                        'description': '',
                        'reserved': 2,
                        'contents': {
                            'nestarray': {
                                'type': 'Array',
                                'name': '附加项 关联后选择的字段',
                                'default': '',
                                'description': '',
                                'reserved': 2,
                                'contents': {
                                    'date': {
                                        'type': 'Date',
                                        'name': '备份截止日',
                                        'default': '',
                                        'description': '',
                                        'reserved': 2
                                    }
                                }
                            }
                        }
                    }
                },
                'type': 'Array',
                'name': '选择字段',
                'default': '',
                'description': '',
                'reserved': 2
            },
            # Object type
            'limit': {
                'contents': {
                    'date': {
                        'type': 'Date',
                        'name': '备份截止日',
                        'default': '',
                        'description': '',
                        'reserved': 2
                    },
                    'count': {
                        'type': 'Number',
                        'name': '备份次数',
                        'default': '',
                        'description': '',
                        'reserved': 2
                    }
                },
                'type': 'Object',
                'name': '限制',
                'default': '',
                'description': '',
                'reserved': 2
            }
        }
