import inspect

from light.cache import Cache
from light.constant import Const
from light.model.data import Data
from light.mongo.controller import Controller

CONST = Const()
RIDER_INSTANCE = None
METHODS = [None, 'add', 'update', 'remove', 'list', 'search', 'get', 'count', 'upsert']


class Rider(object):
    def __init__(self):
        boards = Cache.instance().get(CONST.SYSTEM_DB_BOARD)
        structures = Cache.instance().get(CONST.SYSTEM_DB_STRUCTURE)

        # Add default schema instance
        for structure in structures:
            schema = structure['schema']
            if not hasattr(self, schema):
                setattr(self, schema, Schema(structure=structure))

        # Use action of board to replace the schema instance method
        for board in boards:
            schema = board['class']
            action = board['action']
            type = board['type']
            if hasattr(self, schema):
                data = Data(board)
                setattr(getattr(self, schema), action, getattr(data, METHODS[type]))

    @staticmethod
    def instance():
        global RIDER_INSTANCE

        if not RIDER_INSTANCE:
            RIDER_INSTANCE = Rider()

        return RIDER_INSTANCE

    @staticmethod
    def create_user(handler):
        return Controller(handler=handler).create_user()

    @staticmethod
    def add_user(handler):
        return Controller(handler=handler).add_user()

    @staticmethod
    def drop_user(handler):
        return Controller(handler=handler).drop_user()

    @staticmethod
    def change_password(handler):
        return Controller(handler=handler).change_password()

    @staticmethod
    def drop(handler):
        return Controller(handler=handler).drop()

    @staticmethod
    def aggregate(handler):
        return Controller(handler=handler).aggregate()

    @staticmethod
    def increment(handler):
        return Controller(handler=handler).increment()

    @staticmethod
    def read_file_from_grid(handler):
        return Controller(handler=handler).read_file_from_grid()

    @staticmethod
    def read_stream_from_grid(handler):
        return Controller(handler=handler).read_stream_from_grid()

    @staticmethod
    def write_file_to_grid(handler):
        return Controller(handler=handler).write_file_to_grid()

    @staticmethod
    def write_stream_to_grid(handler):
        return Controller(handler=handler).write_stream_to_grid()


class Schema(object):
    def __init__(self, structure=None, board=None):
        self.board = board
        self.structure = structure

    def data(self):
        if self.board:
            return Data(self.board)

        # Get parent function name
        outer = inspect.getouterframes(inspect.currentframe(), 2)
        action = outer[1][3]

        board = {'action': action, 'class': self.structure['schema'], 'filters': [], 'selects': []}

        # Create default selects
        if action in ['get', 'list', 'count']:
            board['selects'] = [{'key': k, 'select': True} for k, v in self.structure['items'].items()]

        if action in ['update', 'remove', 'upsert']:
            board['selects'] = [{'key': '_id', 'select': True}]

        # Create default filters
        if action != 'add':
            board['filters'] = [
                {'group': '0000', 'key': k, 'operator': '$eq', 'parameter': k, 'default': ''}
                for k, v in self.structure['items'].items()]

        return Data(board)

    def get(self, handler, params=None):
        return self.data().get(handler, params)

    def list(self, handler, params=None):
        return self.data().list(handler, params)

    def count(self, handler, params=None):
        return self.data().count(handler, params)

    def update(self, handler, params=None):
        return self.data().update(handler, params)

    def remove(self, handler, params=None):
        return self.data().remove(handler, params)

    def search(self, handler, params=None):
        return self.data().search(handler, params)

    def upsert(self, handler, params=None):
        return self.data().upsert(handler, params)

    def add(self, handler):
        return self.data().add(handler)
