from light.mongo.type import *


class Mapping(object):
    @staticmethod
    def parse_data(data, defines):
        if isinstance(data, dict):
            data = [data]

        for datum in data:

            for key, val in datum.items():

                # If the key contains mongodb operator, ex. {$set: {field: val}}
                if key.startswith('$'):
                    UpdateOperator.parse(key, val, defines)
                    continue

                define = getattr(defines, key)

                # Is dict, then recursion
                if isinstance(val, dict):
                    if isinstance(define.contents, dict):
                        Mapping.parse_data(val, define.contents)
                        continue

                    # The val contains mongodb operator
                    # TODO
                    continue

                # Is list, then recursion
                if isinstance(val, list):
                    if isinstance(define.contents, Items):
                        Mapping.parse_data(val, define.contents)
                        continue

                    # TODO
                    datum[key] = globals()[define.contents].parse(val)
                    continue

                # Parse value
                datum[key] = globals()[define.type].parse(val)

    def parse_query(self, query, define):
        pass


class Items(object):
    def __init__(self, key, items):
        self._key = key
        self._items = {}

        if isinstance(items, dict):
            for key, item in items.items():
                self._items[key] = Item(key, item)
        else:
            self._items[key] = items

    @property
    def key(self):
        return self._key

    @property
    def items(self):
        return self._items

    def __getattr__(self, key):
        if key in self._items:
            return self._items[key]
        return None


class Item(object):
    """
    key         标识
    type        数据类型
    name        逻辑名称
    reserved    是否为内建数据类型
    default     缺省值
    description 描述
    contents    项目为 Object 类型时, 使用 contents 来描述子项目
                项目为 Array 类型时, 子项目为 Object 类型, 使用 contents 来描述子项目
                项目为 Array 类型时, 子项目为单一类型, 使用 contents 来描述子项目的数据类型
    """

    def __init__(self, key, item):
        self._key = key
        self._reserved = item['reserved']
        self._type = item['type']
        self._name = item['name']
        if 'default' in item:
            self._default = item['default']
        if 'description' in item:
            self._description = item['description']
        if 'contents' in item:
            if isinstance(item['contents'], str):
                self._contents = item['contents']
            else:
                self._contents = Items(key, item['contents'])

    @property
    def key(self):
        return self._key

    @property
    def type(self):
        return self._type

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def default(self):
        return self._default

    @property
    def description(self):
        return self._description

    @property
    def reserved(self):
        return self._reserved

    @property
    def contents(self):
        return self._contents


class UpdateOperator(object):
    @staticmethod
    def parse(name, data, defines):
        getattr(UpdateOperator, name[1:])(data, defines)

    """
    Field Update Operators
    """

    @staticmethod
    def inc(data, defines):
        # { $inc: { <field1>: <amount1>, <field2>: <amount2>, ... } }
        Mapping.parse_data(data, defines)

    @staticmethod
    def mul(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def rename(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def setOnInsert(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def set(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def unset(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def min(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def max(data, defines):
        Mapping.parse_data(data, defines)

    @staticmethod
    def currentDate(data, defines):
        # { $currentDate: { <field1>: <typeSpecification1>, ... } }
        pass

    """
    Array Update Operators
    """

    @staticmethod
    def addToSet(data, defines):
        # { $addToSet: { <field1>: <value1>, ... } }
        Mapping.parse_data(data, defines)

    @staticmethod
    def pop(data, defines):
        # { $pop: { <field>: <-1 | 1>, ... } }
        pass

    @staticmethod
    def pullAll(data, defines):
        # { $pullAll: { <field1>: [ <value1>, <value2> ... ], ... } }
        Mapping.parse_data(data, defines)

    @staticmethod
    def pull(data, defines):
        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }
        # TODO: convert condition
        Mapping.parse_data(data, defines)

    @staticmethod
    def pushAll(data, defines):
        # { $pushAll: { <field>: [ <value1>, <value2>, ... ] } }
        Mapping.parse_data(data, defines)

    @staticmethod
    def push(data, defines):
        # { $push: { <field1>: <value1>, ... } }
        Mapping.parse_data(data, defines)

    @staticmethod
    def each(data, defines):
        # { $push: { <field>: { $each: [ <value1>, <value2> ... ] } } }
        # TODO: convert each value
        pass

    @staticmethod
    def slice(data, defines):
        # { $push: { <field>: { $each: [ <value1>, <value2>, ... ], $slice: <num> } } }
        pass

    @staticmethod
    def sort(data, defines):
        # { $push: { <field>: { $each: [ <value1>, <value2>, ... ], $sort: <sort specification> } } }
        pass

    @staticmethod
    def position(data, defines):
        # { $push: { <field>: { $each: [ <value1>, <value2>, ... ], $position: <num> } } }
        pass

    """
    Bitwise Update Operators
    """

    @staticmethod
    def bit(data, defines):
        # { $bit: { <field>: { <and|or|xor>: <int> } } }
        pass

    """
    Isolation Update Operators
    """

    @staticmethod
    def isolated(data, defines):
        pass


class QueryOperators(object):
    """
    Comparison Query Operators
    """

    @staticmethod
    def _eq(self):
        # { <field>: { $eq: <value> } }
        pass

    @staticmethod
    def _gt(self):
        pass

    @staticmethod
    def _gte(self):
        pass

    @staticmethod
    def _lt(self):
        pass

    @staticmethod
    def _lte(self):
        pass

    @staticmethod
    def _ne(self):
        # { field: {$ne: value} }
        pass

    @staticmethod
    def _in(self):
        # { field: { $in: [<value1>, <value2>, ... <valueN> ] } }TODO
        pass

    @staticmethod
    def _nin(self):
        pass

    """
    Logical Query Operators
    """

    @staticmethod
    def _or(self):
        # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
        pass

    @staticmethod
    def _and(self):
        # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        pass

    @staticmethod
    def _not(self):
        # { field: { $not: { <operator-expression> } } }
        pass

    @staticmethod
    def _nor(self):
        # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        pass

    """
    Element Query Operators
    """

    def _exists(self):
        # { field: { $exists: <boolean> } }
        pass

    def _type(self):
        # { field: { $type: <BSON type number> | <String alias> } }
        pass

    """
    Evaluation Query Operators
    """

    def _mod(self):
        # { field: { $mod: [ divisor, remainder ] } }
        pass

    def _regex(self):
        # { <field>: { $regex: /pattern/, $options: '<options>' } }
        pass

    def _text(self):
        # {
        #   $text: {
        #     $search: <string>,
        #     $language: <string>,
        #     $caseSensitive: <boolean>,
        #     $diacriticSensitive: <boolean>
        #   }
        # }
        pass

    def _where(self):
        pass

    """
    Geospatial Query Operators
    """

    """
    Query Operator Array
    """

    def _all(self):
        # { <field>: { $all: [ <value1> , <value2> ... ] } }
        pass

    def _elemMatch(self):
        # { <field>: { $elemMatch: { <query1>, <query2>, ... } } }
        pass

    def _size(self):
        pass

    """
    Bitwise Query Operators
    """

    def _bitsAllSet(self):
        pass

    def _bitsAnySet(self):
        pass

    def _bitsAllClear(self):
        pass

    def _bitsAnyClear(self):
        pass

    """
    Projection Operators
    """

    def _meta(self):
        # { $meta: <metaDataKeyword> }
        pass

    def _slice(self):
        # db.collection.find( { field: value }, { array: {$slice: count } } );
        pass

    def _comment(self):
        pass


class AggregationOperators(object):
    pass
