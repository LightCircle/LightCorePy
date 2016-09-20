from light.mongo.type import *
from light.mongo.define import Items


class Type(object):
    @staticmethod
    def convert(val):
        if val == 1 or val == '1':
            return 'double'
        elif val == 2 or val == '2':
            return 'string'
        elif val == 3 or val == '3':
            return 'object'
        elif val == 4 or val == '4':
            return 'array'
        elif val == 5 or val == '5':
            return 'binData'
        elif val == 6 or val == '6':
            return 'undefined'
        elif val == 7 or val == '7':
            return 'objectId'
        elif val == 8 or val == '8':
            return 'bool'
        elif val == 9 or val == '9':
            return 'date'
        elif val == 10 or val == '10':
            return 'null'
        elif val == 11 or val == '11':
            return 'regex'
        elif val == 12 or val == '12':
            return 'dbPointer'
        elif val == 13 or val == '13':
            return 'javascript'
        elif val == 14 or val == '14':
            return 'symbol'
        elif val == 15 or val == '15':
            return 'javascriptWithScope'
        elif val == 16 or val == '16':
            return 'int'
        elif val == 17 or val == '17':
            return 'timestamp'
        elif val == 18 or val == '18':
            return 'long'
        elif val == -1 or val == '-1':
            return 'minKey'
        elif val == 127 or val == '127':
            return 'maxKey'
        else:
            return val

    @staticmethod
    def parse(data):
        return Type.convert(data)

    @staticmethod
    def compare(operator, field=None, value=None):
        if operator == '$or':
            return {'$or': value}

        return {field: {operator: value}}


class ReadDotDefine(object):
    @staticmethod
    def dotparse(key, define):
        if not isinstance(key, str):
            return None

        if key.count('.') == 0:
            return define.get(key)

        datum = key.split('.')

        for index, val in enumerate(datum):
            define_cache = None
            if isinstance(define, Items):
                define_cache = define.get(val)
            elif isinstance(define.contents, Items):
                define_cache = define.contents.get(val)

            if define_cache is None:
                continue

            define = define_cache

        return define


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
        for key, val in data.items():
            data[key] = String.parse(val)

    @staticmethod
    def _setOnInsert(data, defines):
        # { $setOnInsert: { <field1>: <value1>, ... } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _set(data, defines):
        # { $set: { <field1>: <value1>, ... } }
        # case I:   defines.contnents == None + defines.type == var or
        #           defines.contnents == var + defines.type == Array
        #           e.x. {'$set': {'schema': 1}}
        # case II:  defines.contents == {} + defines.type == Object or
        #           defines.contents == {} + defines.type == Array or
        #           defines.contents == {nest} + defines.type == Object or
        #           defines.contents == {nest} + defines.type == Array
        #           e.x. {'$set': {'limit': {'date': '2006/01/01', 'count': '1'}}}
        #           e.x. {'$set': {'selects': [{'select': 0, 'fields': [{'nest': 2}, {'nest': 3}]}, {'select': 1}]}}
        #           e.x. {'$set': {'selects': [{'select': 0, 'fields': [1, 2]}, {'select': 1}]}}
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            if define is not None and not isinstance(define.contents, Items):
                if define.type != 'Array':
                    data[key] = globals()[define.type].parse(val)
                else:
                    data[key] = globals()[define.contents].parse(val)
                continue

            if isinstance(val, list):
                for index, datum in enumerate(val):
                    getattr(UpdateOperator, '_set')(val[index], define.contents)
                continue

            if isinstance(val, dict):
                getattr(UpdateOperator, '_set')(val, define.contents)
                continue

    @staticmethod
    def _unset(data, defines):
        # { $unset: { <field1>: '', ... } }
        for key, val in data.items():
            data[key] = ''

    @staticmethod
    def _min(data, defines):
        # { $min: { <field1>: <value1>, ... } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _max(data, defines):
        # { $max: { <field1>: <value1>, ... } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _currentDate(data, defines):
        # { $currentDate: { <field1>: <typeSpecification1>, ... } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            if isinstance(val, dict):
                for k, v in val.items():
                    dict_cache = {k: v}
                    val[k] = getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                    val[k] = dict_cache[k]
                continue

            data[key] = Boolean.parse(val)

    """
    Array Update Operators
    """

    @staticmethod
    def _addToSet(data, defines):
        # { $addToSet: { <field1>: <value1>, ... } }
        # { $addToSet: { <field1>: { <modifier1>: <value1>, ... }, ... } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
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
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _pull(data, defines):
        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }
        # case I:   defines.get(key).contents is val
        #           { $pull: { fruits: { $ in: ['apples', 'oranges']}, vegetables: 'carrots'}}
        # case II:  defines.get(key).contents is Items
        #           { $pull: { results: { $elemMatch: { score: 8 , item: 'B' } } } }
        #           { $pull: { results: { answers: { $elemMatch: { q: 2, a: { $gte: 8 } } } } } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            if define is not None and isinstance(define.contents, Items):
                for k, v in val.items():
                    dict_cache = {k: v}
                    if k is not None and k.startswith('$'):
                        getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                        val[k] = dict_cache[k]
                        continue

                    getattr(UpdateOperator, '_pull')(dict_cache, define.contents)
                    val[k] = dict_cache[k]
                continue

            if isinstance(val, dict):
                for k, v in val.items():
                    if k is not None and k.startswith('$'):
                        dict_cache = {k: v}
                        getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                        val[k] = dict_cache[k]
                continue

            data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _pushAll(data, defines):
        # { $pushAll: { <field>: [ <value1>, <value2>, ... ] } }
        # Update.parse_data(data)
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
            data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _push(data, defines):
        # { $push: { <field1>: <value1>, ... } }
        # { $push: { <field1>: { <modifier1>: <value1>, ... }, ... } }
        for key, val in data.items():
            # define = defines.get(key)
            define = ReadDotDefine.dotparse(key, defines)
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
        if isinstance(define.contents, Items):
            for index, val in enumerate(data):
                for k, v in val.items():
                    defin = define.contents.get(k)
                    if isinstance(defin.contents, Items):
                        if isinstance(v, dict):
                            getattr(UpdateOperator, '_each')([data[index][k]], defin)
                        elif isinstance(v, list):
                            getattr(UpdateOperator, '_each')(data[index][k], defin)
                        continue

                    if defin.type != 'Array':
                        data[index][k] = globals()[defin.type].parse(v)
                    else:
                        data[index][k] = globals()[defin.contents].parse(v)
        else:
            data = globals()[define.contents].parse(data)
        return data

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
    def _eq(data, define):
        # { <field>: { $eq: <value> } }
        # { <field>: <value> }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _gt(data, define):
        # { field: {$gt: value} }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _gte(data, define):
        # { field: {$gte: value} }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _lt(data, define):
        # { field: {$lt: value} }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _lte(data, define):
        # { field: {$lte: value} }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _ne(data, define):
        # { field: {$ne: value} }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _in(data, define):
        # { field: { $in: [<value1>, <value2>, ... <valueN> ] } }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    @staticmethod
    def _nin(data, define):
        # { field: { $nin: [<value1>, <value2>, ... <valueN> ] } }
        for key, val in data.items():
            if define.type != 'Array':
                data[key] = globals()[define.type].parse(val)
            else:
                data[key] = globals()[define.contents].parse(val)

    """
    Logical Query Operators
    """

    @staticmethod
    def _or(data, defines):
        # { $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
        for datum in data:
            for key, val in datum.items():
                # define = defines.get(key)
                define = ReadDotDefine.dotparse(key, defines)
                if isinstance(val, dict):
                    for k, v in val.items():
                        # val[k] = globals()[define.type].parse(v)
                        if k is not None and k.startswith('$'):
                            dict_cache = {k: v}
                            getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                            val[k] = dict_cache[k]
                    continue

                datum[key] = globals()[define.type].parse(val)

    @staticmethod
    def _and(data, defines):
        # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        for datum in data:
            for key, val in datum.items():
                # $and + $or
                if key is not None and key.startswith('$'):
                    getattr(QueryOperator, key.replace('$', '_'))(val, defines)
                    continue

                # define = defines.get(key)
                define = ReadDotDefine.dotparse(key, defines)
                if isinstance(val, dict):
                    for k, v in val.items():
                        if k is not None and k.startswith('$'):
                            dict_cache = {k: v}
                            getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                            val[k] = dict_cache[k]
                    continue

                datum[key] = globals()[define.type].parse(val)

    @staticmethod
    def _not(data, define):
        # { field: { $not: { <operator-expression> } } }
        for key, val in data.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    dict_cache = {k: v}
                    getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                    val[k] = dict_cache[k]
                continue

            data[key] = globals()[define.type].parse(val)

    @staticmethod
    def _nor(data, defines):
        # { $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
        for datum in data:
            for key, val in datum.items():

                # define = defines.get(key)
                define = ReadDotDefine.dotparse(key, defines)

                if isinstance(val, dict):
                    for k, v in val.items():
                        if k is not None and k.startswith('$'):
                            dict_cache = {k: v}
                            getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                            val[k] = dict_cache[k]
                    continue

                datum[key] = globals()[define.type].parse(val)

    """
    Element Query Operators
    """

    @staticmethod
    def _exists(data, define):
        # { field: { $exists: <boolean> } }
        for key, val in data.items():
            data[key] = Boolean.parse(val)

    @staticmethod
    def _type(data, define):
        # { field: { $type: <BSON type number> | <String alias> } }
        for key, val in data.items():
            data[key] = Type.parse(val)

    """
    Evaluation Query Operators
    """

    @staticmethod
    def _mod(data, define):
        # { field: { $mod: [ divisor, remainder ] } }
        for key, val in data.items():
            data[key] = Number.parse(val)

    @staticmethod
    def _regex(data, define):
        # { <field>: { $regex: /pattern/, $options: '<options>' } }
        # { <field>: { $regex: 'pattern', $options: '<options>' } }
        # { <field>: { $regex: /pattern/<options> } }
        for key, val in data.items():
            data[key] = String.parse(val)

    @staticmethod
    def _options(data, define):
        # { <field>: { $regex: /pattern/, $options: '<options>' } }
        # { <field>: { $regex: 'pattern', $options: '<options>' } }
        # { <field>: { $regex: /pattern/<options> } }
        for key, val in data.items():
            data[key] = String.parse(val)

    @staticmethod
    def _text(data, define):
        # {
        #   $text: {
        #     $search: <string>,
        #     $language: <string>,
        #     $caseSensitive: <boolean>,
        #     $diacriticSensitive: <boolean>
        #   }
        # }
        for key, val in data.items():
            if key == '$search' or key == '$language':
                data[key] = String.parse(val)
                continue
            if key == '$caseSensitive' or key == '$diacriticSensitive':
                data[key] = Boolean.parse(val)
                continue

    def _where(self):
        raise NotImplementedError

    """
    Geospatial Query Operators
    """

    """
    Query Operator Array
    """

    @staticmethod
    def _all(data, defines):
        # { <field>: { $all: [ <value1> , <value2> ... ] } }
        # case I:   defines.contents == Items
        #           { <field>: { $all: [{ $elemMatch: { <query1>, <query2>, ... }]}}
        #           { <field>: { $all: [ { <contents_value1> }, { <contents_value2> }, ... ]}}
        #           { <field>: { $all: [ [ { <contents_value1> }, { <contents_value2> }, ... ] , ... ] } }
        # case II:  defines.contents == Var
        #           { <field>: { $all: [ [ <value1>, <value2> ], ... ] } }
        #           { <field>: { $all: [ <value1> , <value2>, ... ] } }
        for key, val in data.items():
            for index, datum in enumerate(val):
                if defines.contents == 'Object':
                    return
                if isinstance(defines.contents, Items):
                    if isinstance(datum, dict):
                        for k, v in datum.items():
                            # $all + $elemMatch
                            if k is not None and k.startswith('$'):
                                getattr(QueryOperator, k.replace('$', '_'))(val[index], defines)
                                continue

                            define = defines.contents.get(k)
                            val[index][k] = globals()[define.type].parse(v)
                            continue
                        continue

                    if isinstance(datum, list):
                        for indexin, datumin in enumerate(datum):
                            for k, v in datumin.items():
                                define = defines.contents.get(k)
                                val[index][indexin][k] = globals()[define.type].parse(v)
                                continue
                        continue

                if isinstance(datum, list):
                    globals()[defines.type].parse(val[index])
                    continue

                val[index] = globals()[defines.type].parse(datum)

                # Method I:
                # for key, val in data.items():
                #     for datum in val:
                #         # { <field>: { $all: [ <value1> , <value2>, ... ] } }
                #         if not isinstance(datum, dict) and not isinstance(datum, list):
                #             globals()[defines.type].parse(val)
                #             return
                #         # { <field>: { $all: [ [ <value1>, <value2> ], ... ] } }
                #         if isinstance(datum, list) and datum and not isinstance(datum[0], dict):
                #             globals()[defines.type].parse(datum)
                #             continue
                #         # {<field>: { $all: [ [ { <contents_value1> }, { <contents_value2> }, ... ] , ... ] } }
                #         if isinstance(datum, list) and datum and isinstance(datum[0], dict):
                #             for datum_sub in datum:
                #                 for k_sub, v_sub in datum_sub.items():
                #                     if defines is not None and isinstance(defines.contents, Items):
                #                         define = defines.contents.get(k_sub)
                #                         datum_sub[k_sub] = globals()[define.type].parse(v_sub)
                #                         continue
                #             continue
                #         if isinstance(datum, dict):
                #             for k, v in datum.items():
                #                 # $all + $elemMatch
                #                 # {<field>: { $all: [{ $elemMatch: { <query1>, <query2>, ... }]}}
                #                 if k is not None and k.startswith('$'):
                #                     getattr(QueryOperator, k.replace('$', '_'))(datum, defines)
                #                     continue
                #                 # {<field>: { $all: [ { <contents_value1> }, { <contents_value2> }, ... ]}}
                #                 if defines is not None and isinstance(defines.contents, Items):
                #                     define = defines.contents.get(k)
                #                     datum[k] = globals()[define.type].parse(v)
                #                     continue

    @staticmethod
    def _elemMatch(data, defines):
        # { <field>: { $elemMatch: { <query1>, <query2>, ... } } }
        # case I:   defines.contents == Items
        #           e.x. { results: { $elemMatch: { product: 'xyz', score: { $gte: 8 } } } }
        # case II:  defines.contents == Var
        #           e.x. { results: { $elemMatch: { $gte: 80, $lt: 85 } } }
        for key, val in data.items():
            if isinstance(defines, Items):
                # define = defines.get(key)
                define = ReadDotDefine.dotparse(key, defines)
                if define is not None and isinstance(define.contents, Items):
                    getattr(QueryOperator, '_elemMatch')(val, define.contents)
                    continue

                if isinstance(val, dict):
                    for k, v in val.items():
                        if k is not None and k.startswith('$'):
                            dict_cache = {k: v}
                            getattr(QueryOperator, k.replace('$', '_'))(dict_cache, define)
                            val[k] = dict_cache[k]
                    continue

                data[key] = globals()[define.type].parse(val)
                # if define.type != 'Array':
                #    data[key] = globals()[define.type].parse(val)
                # else:
                #    data[key] = globals()[define.contents].parse(val)
                continue

            if isinstance(defines.contents, Items):
                getattr(QueryOperator, '_elemMatch')(val, defines.contents)
                continue

            for k, v in val.items():
                if k is not None and k.startswith('$'):
                    dict_cache = {k: v}
                    getattr(QueryOperator, k.replace('$', '_'))(dict_cache, defines)
                    val[k] = dict_cache[k]

                    # Mathod I:
                    # for k, v in val.items():
                    #     # e.x. { results: { $elemMatch: { $gte: 80, $lt: 85 } } }
                    #     if k is not None and k.startswith('$'):
                    #         val[k] = globals()[defines.type].parse(v)
                    #         continue
                    #     # e.x. { results: { $elemMatch: { product: 'xyz', score: { $gte: 8 } } } }
                    #     if isinstance(defines.contents, Items):
                    #         define = defines.contents.get(k)
                    #         val[k] = globals()[define.type].parse(v)
                    #         continue

    @staticmethod
    def _size(data, defines):
        # { < field >: { $size: < number > } }
        Number.parse(data)

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
