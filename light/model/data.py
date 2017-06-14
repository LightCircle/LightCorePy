"""
排序的设计:
    排序结果是 handler.params.sort + board.sort
    参数中指定的sort优先
    sort的写法是 { a: 'asc', b: 'desc' } 或 { a: 1, b: -1 }
"""

from operator import itemgetter
from datetime import datetime, date
from light.constant import Const
from light.mongo.controller import Controller
from light.mongo.operator import Type

CONST = Const()


class Data(object):
    def __init__(self, board):
        self.board = board
        self.table = self.board['class']

    def get(self, handler, params=None):
        if params is not None:
            handler.set_params(params)

        handler.params.condition = get_filter(handler, self.board)

        data, error = Controller(handler=handler, table=self.table).get()
        return data, error

    def list(self, handler, params=None):
        if params is not None:
            handler.set_params(params)

        handler.params.condition = get_filter(handler, self.board)
        handler.params.sort = get_order(handler, self.board)

        data, error = Controller(handler=handler, table=self.table).list()
        return data, error

    def add(self, handler):
        data, error = Controller(handler=handler, table=self.table).add()
        return data, error

    def update(self, handler, params=None, upsert=False):
        if params is not None:
            handler.set_params(params)

        handler.params.condition = get_filter(handler, self.board)

        data, error = Controller(handler=handler, table=self.table).update(upsert)
        return data, error

    def upsert(self, handler, params=None):
        return self.update(handler, params, True)

    def remove(self, handler, params=None):
        if params is not None:
            handler.set_params(params)

        handler.params.condition = get_filter(handler, self.board)

        data, error = Controller(handler=handler, table=self.table).remove()
        return data, error

    def count(self, handler, params=None):
        if params is not None:
            handler.set_params(params)

        handler.params.condition = get_filter(handler, self.board)

        data, error = Controller(handler=handler, table=self.table).count()
        return data, error

    def search(self, handler, params=None):
        raise NotImplementedError


def get_order(handler, board):

    # Sort by index item
    sorts = sorted(board['sorts'], key=itemgetter('index'))

    # Convert data format, and combined with user-specified content
    order = handler.params.sort or {}
    sorts = {i['key']: i['order'] for i in sorts if i['key'] not in order}

    return {**order, **sorts}


def get_filter(handler, board):
    if handler.params.free is not None:
        return handler.params.free

    data = handler.params.condition or {}
    or_condition = {}

    for f in board['filters']:
        parameter = f['parameter']
        operator = f['operator']
        key = f['key']
        group = f['group']
        if 'default' in f:
            default = f['default']

        if group not in or_condition:
            or_condition[group] = {}

        value = None
        and_condition = or_condition[group]

        # If the parameter is not specified, the default value
        if not parameter and default:
            value = get_reserved(handler, default)
        else:
            if parameter in data:
                value = data[parameter]

            # Can not get to the parameter value, the default value
            if value is None and default:
                value = get_reserved(handler, default)

        if value is None:
            continue

        compare = Type.compare(operator, key, value)
        and_condition.update(compare)

    # No condition to return empty
    or_condition = list(or_condition.values())
    if len(or_condition) < 1:
        return {}

    # If only one condition or group, are removed or comparison operators
    if len(or_condition) == 1:
        return or_condition[0]

    # Removing empty condition
    return Type.compare('$or', value=or_condition)


def get_reserved(handler, keyword):
    if keyword == '$uid':
        return handler.uid

    if keyword == '$sysdate':
        return date.today()

    if keyword == '$systime':
        return datetime.now()

    if keyword == '$corp':
        return handler.corp

    return keyword
