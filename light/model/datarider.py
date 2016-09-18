from light.cache import Cache
from light.constant import Const
from light.model.data import Data
from light.mongo.controller import Controller

CONST = Const()
RIDER_INSTANCE = None


class Rider(object):
    def __init__(self):
        boards = Cache.instance().get(CONST.SYSTEM_DB_BOARD)

        for board in boards:
            schema = board['class']
            action = board['action']
            if not hasattr(self, schema):
                setattr(self, schema, Schema())

            data = Data(board)
            if hasattr(data, action):
                setattr(getattr(self, schema), action, getattr(data, action))

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


class Schema(object):
    pass
