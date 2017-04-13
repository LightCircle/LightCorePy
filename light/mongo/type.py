import datetime
import dateutil.parser
import re

from datetime import datetime, date
from bson import ObjectId


class Object(object):
    @staticmethod
    def parse(data):
        return data


class Array(object):
    @staticmethod
    def parse(data):
        return data


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
        if isinstance(val, re._pattern_type):
            return val
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
