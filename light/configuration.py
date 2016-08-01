from light.constant import Const
from light.cache import Cache

CONST = Const()


class Config(object):
    def __init__(self):
        config = Cache.instance().get(CONST.SYSTEM_DB_CONFIG)
        print(config)
