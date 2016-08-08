import light.helper

from light.cache import Cache
from light.constant import Const

CONST = Const()


def dispatch(app):
    bind_api(app)
    bind_route(app)


def bind_api(app):
    boards = Cache.instance().get(CONST.SYSTEM_DB_BOARD)

    for board in boards:

        clazz = light.helper.resolve(board['class'])
        func = light.helper.resolve(board['action'])
        api = light.helper.resolve(board['api'])

        # try lookup controllers class
        if clazz:
            if getattr(clazz, func):
                app.add_url_rule(api, endpoint='{0}#{1}'.format(clazz, func), view_func=func)

        # try lookup system class

        # try lookup data rider


def bind_route(app):
    route = Cache.instance().get(CONST.SYSTEM_DB_ROUTE)

    # try lookup controllers class

    # render html
