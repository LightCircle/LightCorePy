from light.constant import Const
from light.cache import Cache
from light.mongo import type

CONST = Const()
CONFIG_INSTANCE = None


class Config(object):
    """
    Convert configuration data to object property
    """

    def __init__(self):

        self.dictionary = {}
        config = Cache.instance().get(CONST.SYSTEM_DB_CONFIG)

        for item in config:
            key = item['type']
            if hasattr(self, key):
                getattr(self, key).add_children(item)
            else:
                attr = Item()
                attr.add_children(item)
                setattr(self, key, attr)

    @staticmethod
    def instance():
        global CONFIG_INSTANCE

        if not CONFIG_INSTANCE:
            CONFIG_INSTANCE = Config()

        return CONFIG_INSTANCE


class Item(object):
    def __init__(self):
        self.dictionary = {}

    def __getattr__(self, key):
        if key in self.dictionary:
            target = self.dictionary[key]

            if isinstance(target, Item):
                return target

            return self.convert_type(target)

        return None

    def add_children(self, item):
        key = item['key']

        # is single layer property : e.g. 'a' = 'my string'
        if '.' not in key:
            self.dictionary[key] = item
            return

        # is multilayer property : e.g. 'a.b.c' = 'my string'
        key, sub_keys = key.split('.', 1)

        if key not in self.dictionary:
            self.dictionary[key] = Item()

        item['key'] = sub_keys
        self.dictionary[key].add_children(item)

    @staticmethod
    def convert_type(target):
        if target['valueType'] == 'string':
            return str(target['value'])

        if target['valueType'] == 'number':
            if '.' in target['value']:
                return float(target['value'])
            return type.Number.parse(target['value'])

        if target['valueType'] == 'boolean':
            return type.Boolean.convert(target['value'])

        if target['valueType'] == 'array':
            return target['value']

        return None
