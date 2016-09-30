"""
define.py
"""


class Items(object):
    def __init__(self, items):
        self._items = []

        if items is None:
            return

        for item in items:
            self._items.append(Item(item))

    def get(self, key):
        return [item for item in self._items if item.name in key]

    @property
    def items(self):
        return self._items


class Item(object):
    def __init__(self, item):
        self._name = item['name']
        self._rule = item['rule']
        self._key = item['key']
        self._group = None
        self._message = None
        self._option = None

        if 'group' in item:
            self._group = item['group']
        if 'message' in item:
            self._message = item['message']
        if 'option' in item:
            self._option = item['option']

    @property
    def name(self):
        return self._name

    @property
    def rule(self):
        return self._rule

    @property
    def key(self):
        return self._key

    @property
    def group(self):
        return self._group

    @property
    def message(self):
        return self._message

    @property
    def option(self):
        return self._option
