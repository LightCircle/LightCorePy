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

                # If the define not found, then parse next
                if define is None:
                    continue

                # If the val contains mongodb operator, then recursion
                if isinstance(val, str) and val.startswith('$'):
                    UpdateOperator.parse(key, val, Items(key, define))

                # Is dict, then recursion
                if isinstance(val, dict):
                    Mapping.parse_data(val, define.contents)
                    continue

                # Is list, then recursion
                if isinstance(val, list):
                    if isinstance(define.contents, dict):
                        Mapping.parse_data(val, define.contents)
                        continue

                # Parse value todo: parse array
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
            self._items[items.key] = items

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

    '''
    Field Update Operators
    '''

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

    '''
    Array Update Operators
    '''

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
        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }TODO:condition
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
        Mapping.parse_data(data, defines)

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

    '''
    Bitwise Update Operators
    '''

    @staticmethod
    def bit(data, defines):
        # { $bit: { <field>: { <and|or|xor>: <int> } } }
        pass

    '''
    Isolation Update Operators
    '''

    @staticmethod
    def isolated(data, defines):
        pass


class QueryOperators(object):
    def eq(self):
        pass

    def gt(self):
        pass


class AggregationOperators(object):
    pass
