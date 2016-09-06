import datetime
import dateutil.parser

from datetime import datetime, date
from bson import ObjectId


class Object(object):
    pass


class Array(object):
    pass


class Boolean(object):
    @staticmethod
    def convert(val):
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            if val.lower() == 'true':
                return True
            if val.lower() == 'false' or val == '0':
                return False
        return bool(val)

    @staticmethod
    def parse(data):
        if isinstance(data, dict):
            for key, val in data.items():
                data[key] = Boolean.convert(val)
            return data
        if isinstance(data, list):
            return list(map(lambda x: Boolean.convert(x), data))
        return Boolean.convert(data)


class Date(object):
    @staticmethod
    def convert(val):
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        if isinstance(val, date):
            return val
        return dateutil.parser.parse(val)

    @staticmethod
    def parse(data):
        if isinstance(data, dict):
            for key, val in data.items():
                data[key] = Date.convert(val)
            return data
        if isinstance(data, list):
            for index, val in enumerate(data):
                data[index] = Date.convert(val)
            return data
        return Date.convert(data)


class String(object):
    @staticmethod
    def convert(val):
        if val is None:
            return ''
        #if isinstance(val, *):
        #    return val
        return str(val)

    @staticmethod
    def parse(data):
        if isinstance(data, dict):
            for key, val in data.items():
                data[key] = String.convert(val)
            return data
        if isinstance(data, list):
            for index, val in enumerate(data):
                data[index] = String.convert(val)
            return data
        return String.convert(data)


class Number(object):
    @staticmethod
    def convert(val):
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return val
        if isinstance(val, str):
            if '.' in val:
                return float(val)
            return int(val)
        return None

    @staticmethod
    def parse(data):
        if isinstance(data, dict):
            for key, val in data.items():
                data[key] = Number.convert(val)
            return data
        if isinstance(data, list):
            for index, val in enumerate(data):
                data[index] = Number.convert(val)
            return data
        return Number.convert(data)


class ObjectID(object):
    @staticmethod
    def convert(val):
        if isinstance(val, ObjectId):
            return val
        if isinstance(val, str):
            return ObjectId(val)
        return None

    @staticmethod
    def parse(data):
        if isinstance(data, dict):
            for key, val in data.items():
                data[key] = ObjectID.convert(val)
            return data
        if isinstance(data, list):
            return list(map(lambda x: ObjectID.convert(x), data))
        return ObjectID.convert(data)


class Type(object):
    @staticmethod
    def convert(val):
        if val == 1 or val == '1':
            return "double"
        elif val == 2 or val == '2':
            return "string"
        elif val == 3 or val == '3':
            return "object"
        elif val == 4 or val == '4':
            return "array"
        elif val == 5 or val == '5':
            return "binData"
        elif val == 6 or val == '6':
            return "undefined"
        elif val == 7 or val == '7':
            return "objectId"
        elif val == 8 or val == '8':
            return "bool"
        elif val == 9 or val == '9':
            return "date"
        elif val == 10 or val == '10':
            return "null"
        elif val == 11 or val == '11':
            return "regex"
        elif val == 12 or val == '12':
            return "dbPointer"
        elif val == 13 or val == '13':
            return "javascript"
        elif val == 14 or val == '14':
            return "symbol"
        elif val == 15 or val == '15':
            return "javascriptWithScope"
        elif val == 16 or val == '16':
            return "int"
        elif val == 17 or val == '17':
            return "timestamp"
        elif val == 18 or val == '18':
            return "long"
        elif val == -1 or val == '-1':
            return "double"
        elif val == 127 or val == '127':
            return "minKey"
        elif val == 1 or val == '1':
            return "maxKey"
        else:
            return val

    @staticmethod
    def parse(data):
        return Type.convert(data)
