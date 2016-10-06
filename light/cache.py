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
        select = 'type, key, value, valueType'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_CONFIG)
        self.cache.set(CONST.SYSTEM_DB_CONFIG, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        # validator
        select = 'group,name,rule,key,option,message,sanitize,class,action,condition'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_VALIDATOR)
        self.cache.set(CONST.SYSTEM_DB_VALIDATOR, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        # i18n
        select = 'type,lang,key'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_I18N)
        self.cache.set(CONST.SYSTEM_DB_I18N, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        # structure
        select = 'public,lock,type,kind,tenant,version,schema,items,extend,tenant'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_STRUCTURE)
        self.cache.set(CONST.SYSTEM_DB_STRUCTURE, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        # board
        select = 'schema,api,type,kind,path,class,action,filters,selects,sorts,reserved,script'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_BOARD)
        self.cache.set(CONST.SYSTEM_DB_BOARD, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        # route
        select = 'template,url,class,action'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_ROUTE)
        self.cache.set(CONST.SYSTEM_DB_ROUTE, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        # tenant
        select = 'code,name'
        model = Model(domain=self.domain, code=CONST.SYSTEM_DB_PREFIX, table=CONST.SYSTEM_DB_TENANT)
        self.cache.set(CONST.SYSTEM_DB_TENANT, model.get_by(condition=valid, select=select, limit=CONST.MAX_INT))

        return model.db

    @staticmethod
    def instance():
        global CACHE_INSTANCE

        if not CACHE_INSTANCE:
            CACHE_INSTANCE = LRUCache(100)

        return CACHE_INSTANCE
