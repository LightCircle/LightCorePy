from light.mongo.type import *


class UpdateOperator(object):
    def parse(self, key, val, defines):
        getattr(self, key.replace('$', '_'))(val, defines)

    """
    Field Update Operators
    """

    @staticmethod
    def _inc(data, defines):
        # { $inc: { <field1>: <amount1>, <field2>: <amount2>, ... } }
        Number.parse(data)

    @staticmethod
    def _mul(data, defines):
        # { $mul: { field: <number> } }
        Number.parse(data)

    @staticmethod
    def _rename(data, defines):
        # { $rename: { <field1>: <newName1>, <field2>: <newName2>, ... } }
        String.parse(data)

    @staticmethod
    def _setOnInsert(data, defines):
        # { $setOnInsert: { <field1>: <value1>, ... } }
        raise NotImplementedError

    @staticmethod
    def _set(data, defines):
        # { $set: { <field1>: <value1>, ... } }
        for key, val in data.items():
            define = defines.get(key)
            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _unset(data, defines):
        # { $unset: { <field1>: "", ... } }
        return ''

    @staticmethod
    def _min(data, defines):
        # { $min: { <field1>: <value1>, ... } }
        raise NotImplementedError

    @staticmethod
    def _max(data, defines):
        # { $max: { <field1>: <value1>, ... } }
        raise NotImplementedError

    @staticmethod
    def _currentDate(data, defines):
        # { $currentDate: { <field1>: <typeSpecification1>, ... } }
        pass

    """
    Array Update Operators
    """

    @staticmethod
    def _addToSet(data, defines):
        # { $addToSet: { <field1>: <value1>, ... } }
        # { $addToSet: { <field1>: { <modifier1>: <value1>, ... }, ... } }
        for key, val in data.items():
            define = defines.get(key)

            # support modifier
            if isinstance(val, dict):
                for k, v in val.items():
                    val[k] = getattr(UpdateOperator, k.replace('$', '_'))(v, define)
                continue

            # basic type
            data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _pop(data, defines):
        # { $pop: { <field>: <-1 | 1>, ... } }
        Number.parse(data)

    @staticmethod
    def _pullAll(data, defines):
        # { $pullAll: { <field1>: [ <value1>, <value2> ... ], ... } }
        raise NotImplementedError

    @staticmethod
    def _pull(data, defines):
        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }
        # TODO: convert condition
        raise NotImplementedError

    @staticmethod
    def _pushAll(data, defines):
        # { $pushAll: { <field>: [ <value1>, <value2>, ... ] } }
        # Update.parse_data(data)
        raise NotImplementedError

    @staticmethod
    def _push(data, defines):
        # { $push: { <field1>: <value1>, ... } }
        # { $push: { <field1>: { <modifier1>: <value1>, ... }, ... } }
        for key, val in data.items():
            define = defines.get(key)

            # support modifier
            if isinstance(val, dict):
                for k, v in val.items():
                    val[k] = getattr(UpdateOperator, k.replace('$', '_'))(v, define)
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
    def _bit(data, defines):
        # { $bit: { <field>: { <and|or|xor>: <int> } } }
        pass

    """
    Isolation Update Operators
    """

    @staticmethod
    def _isolated(data, defines):
        pass


class QueryOperator(object):
    def parse(self, key, val, defines):
        getattr(self, key.replace('$', '_'))(val, defines)

    """
    Comparison Query Operators
    """

    @staticmethod
    def _eq(data, defines):
        # { <field>: { $eq: <value> } }
        # { $eq: { <field>: <value> } }
        for key, val in data.items():
            define = defines.get(key)
            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _gt(self):
        # { field: {$gt: value} }
        pass

    @staticmethod
    def _gte(self):
        # { field: {$gte: value} }
        pass

    @staticmethod
    def _lt(self):
        # { field: {$lt: value} }
        pass

    @staticmethod
    def _lte(self):
        # { field: {$lte: value} }
        pass

    @staticmethod
    def _ne(self):
        # { field: {$ne: value} }
        pass

    @staticmethod
    def _in(self):
        # { field: { $in: [<value1>, <value2>, ... <valueN> ] } }
        pass

    @staticmethod
    def _nin(self):
        # { field: { $nin: [<value1>, <value2>, ... <valueN> ] } }
        pass

    """
    Logical Query Operators
    """

    @staticmethod
    def _or(data, defines):
        # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
        for datum in data:
            for key, val in datum.items():
                define = defines.get(key)

                if isinstance(val, dict):
                    for k, v in val.items():
                        val[k] = globals()[define.type].parse(v)
                    continue

                datum[key] = globals()[define.type].parse(val)

    @staticmethod
    def _and(data, defines):
        # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        for datum in data:
            for key, val in datum.items():
                # $and + $or
                if key.startswith('$'):
                    getattr(QueryOperator, key.replace('$', '_'))(val, defines)
                    continue

                define = defines.get(key)

                if isinstance(val, dict):
                    for k, v in val.items():
                        val[k] = globals()[define.type].parse(v)
                    continue

                datum[key] = globals()[define.type].parse(val)

    @staticmethod
    def _not(data, defines):
        # { field: { $not: { <operator-expression> } } }
        raise NotImplementedError

    @staticmethod
    def _nor(data, defines):
        # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        raise NotImplementedError

    """
    Element Query Operators
    """

    def _exists(self):
        # { field: { $exists: <boolean> } }
        raise NotImplementedError

    def _type(self):
        # { field: { $type: <BSON type number> | <String alias> } }
        raise NotImplementedError

    """
    Evaluation Query Operators
    """

    def _mod(self):
        # { field: { $mod: [ divisor, remainder ] } }
        raise NotImplementedError

    def _regex(self):
        # { <field>: { $regex: /pattern/, $options: '<options>' } }
        raise NotImplementedError

    def _text(self):
        # {
        #   $text: {
        #     $search: <string>,
        #     $language: <string>,
        #     $caseSensitive: <boolean>,
        #     $diacriticSensitive: <boolean>
        #   }
        # }
        raise NotImplementedError

    def _where(self):
        raise NotImplementedError

    """
    Geospatial Query Operators
    """

    """
    Query Operator Array
    """

    def _all(self):
        # { <field>: { $all: [ <value1> , <value2> ... ] } }
        raise NotImplementedError

    def _elemMatch(self):
        # { <field>: { $elemMatch: { <query1>, <query2>, ... } } }
        raise NotImplementedError

    def _size(self):
        raise NotImplementedError

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

    def _comment(self):
        pass


class AggregationOperators(object):
    pass
