from bson import ObjectId


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
            if val.lower() == 'false' and val == '0':
                return False
        return bool(val)

    @staticmethod
    def parse(data):
        if isinstance(data, list):
            return list(map(lambda x: Boolean.convert(x), data))
        return Boolean.convert(data)


class Date(object):
    pass


class String(object):
    @staticmethod
    def convert(val):
        if val is None:
            return ''
        return str(val)

    @staticmethod
    def parse(data):
        if isinstance(data, list):
            return list(map(lambda x: String.convert(x), data))
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
        if isinstance(data, list):
            return list(map(lambda x: Number.convert(x), data))
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
        if isinstance(data, list):
            return list(map(lambda x: ObjectID.convert(x), data))
        return ObjectID.convert(data)
