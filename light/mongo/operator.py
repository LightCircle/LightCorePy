from light.mongo.type import *


class UpdateOperator(object):
    def __init__(self):
        self.path = None
        self.defines = None

    def parse(self, key, val, defines, path):
        self.path = path
        self.defines = defines

        getattr(self, key.replace('$', '_'))(val)

    """
    Field Update Operators
    """

    @staticmethod
    def _inc(data):
        # { $inc: { <field1>: <amount1>, <field2>: <amount2>, ... } }
        Number.parse(data)

    @staticmethod
    def _mul(data):
        # { $mul: { field: <number> } }
        Number.parse(data)

    @staticmethod
    def _rename(data):
        # { $rename: { <field1>: <newName1>, <field2>: <newName2>, ... } }
        String.parse(data)

    @staticmethod
    def _setOnInsert(data):
        # { $setOnInsert: { <field1>: <value1>, ... } }
        # define = getattr(defines, key)
        # Update.parse_data(data)
        raise NotImplementedError

    def _set(self, data):
        # { $set: { <field1>: <value1>, ... } }
        for key, val in data.items():
            define = self.defines.get(key)
            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _unset(data):
        # { $unset: { <field1>: "", ... } }
        return ''

    @staticmethod
    def _min(data):
        # { $min: { <field1>: <value1>, ... } }
        # Update.parse_data(data)
        raise NotImplementedError

    @staticmethod
    def _max(data):
        # { $max: { <field1>: <value1>, ... } }
        # Update.parse_data(data)
        raise NotImplementedError

    @staticmethod
    def _currentDate(data):
        # { $currentDate: { <field1>: <typeSpecification1>, ... } }
        pass

    """
    Array Update Operators
    """

    @staticmethod
    def _addToSet(data):
        # { $addToSet: { <field1>: <value1>, ... } }
        # Update.parse_data(data)

        raise NotImplementedError

    @staticmethod
    def _pop(data):
        # { $pop: { <field>: <-1 | 1>, ... } }
        Number.parse(data)

    @staticmethod
    def _pullAll(data):
        # { $pullAll: { <field1>: [ <value1>, <value2> ... ], ... } }
        # Update.parse_data(data)

        raise NotImplementedError

    @staticmethod
    def _pull(data):
        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }
        # TODO: convert condition
        # Update.parse_data(data)
        raise NotImplementedError

    @staticmethod
    def _pushAll(data):
        # { $pushAll: { <field>: [ <value1>, <value2>, ... ] } }
        # Update.parse_data(data)
        raise NotImplementedError

    def _push(self, data):
        # { $push: { <field1>: <value1>, ... } }
        # { $push: { <field1>: { <modifier1>: <value1>, ... }, ... } }
        for key, val in data.items():
            define = self.defines.get(key)

            # support modifier
            if isinstance(val, dict):
                for k, v in val.items():
                    val[k] = getattr(self, k.replace('$', '_'))(v, define)
                continue

            # basic type
            data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _each(data, define):
        # { $push: { <field>: { $each: [ <value1>, <value2> ... ] } } }
        return globals()[define.contents].parse(data)

    @staticmethod
    def _slice(data, define):
        # { $push: { <field>: { $each: [ <value1>, <value2>, ... ], $slice: <num> } } }
        return Number.parse(data)

    @staticmethod
    def _sort(data, define):
        # { $push: { <field>: { $each: [ <value1>, <value2>, ... ], $sort: <sort specification> } } }
        return Number.parse(data)

    @staticmethod
    def _position(data, define):
        # { $push: { <field>: { $each: [ <value1>, <value2>, ... ], $position: <num> } } }
        return Number.parse(data)

    """
    Bitwise Update Operators
    """

    @staticmethod
    def _bit(data):
        # { $bit: { <field>: { <and|or|xor>: <int> } } }
        pass

    """
    Isolation Update Operators
    """

    @staticmethod
    def _isolated(data):
        pass


class QueryOperator(object):
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
