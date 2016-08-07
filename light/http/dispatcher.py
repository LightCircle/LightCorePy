from light.cache import Cache
from light.constant import Const

CONST = Const()


def dispatch():
    bind_api()
    bind_route()


def bind_api():
    board = Cache.instance().get(CONST.SYSTEM_DB_BOARD)

    pass


def bind_route():
    route = Cache.instance().get(CONST.SYSTEM_DB_ROUTE)

    pass
