class Items(object):
    def __init__(self, items):
        self._items = {}

        if items is None:
            return

        for key, item in items.items():
            self._items[key] = Item(key, item)

    def get(self, key):
        if key in self._items:
            return self._items[key]
        return None

    @property
    def items(self):
        return self._items


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
        self._default = None
        self._description = None
        self._contents = None

        if 'default' in item:
            self._default = item['default']
        if 'description' in item:
            self._description = item['description']
        if 'contents' in item:
            if isinstance(item['contents'], dict):
                self._contents = Items(item['contents'])
            else:
                self._contents = item['contents']

    @property
    def key(self):
        return self._key

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
