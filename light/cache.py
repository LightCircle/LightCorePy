import collections
from light.mongo.model import Model
from light.constant import Const

""" Memory-based cache

Cache is a singleton instance of global.
For caching database data.
"""

CONST = Const()
CACHE_INSTANCE = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


class Cache:
    def __init__(self, domain):
        self.domain = domain
        self.cache = Cache.instance()

    def init(self):
        valid = {'valid': 1}

        # configuration
        select = 'group,name,rule,key,option,message,sanitize,class,action,condition'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_CONFIG)
        self.cache.set(CONST.SYSTEM_DB_CONFIG, model.get_by(condition=valid, select=select))

        # structure
        select = 'public,lock,type,kind,tenant,version,schema,items,extend,tenant'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_STRUCTURE)
        self.cache.set(CONST.SYSTEM_DB_CONFIG, model.get_by(condition=valid, select=select))

    @staticmethod
    def instance():
        global CACHE_INSTANCE

        if not CACHE_INSTANCE:
            print(1)
            CACHE_INSTANCE = LRUCache(100)

        return CACHE_INSTANCE
