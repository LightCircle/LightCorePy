from light.constant import Const
from light.mongo.controller import Controller

CONST = Const()


class Data(object):
    def __init__(self, board):
        self.board = board
        self.table = self.board['class']

    def get(self, handler):
        data, error = Controller(handler=handler, table=self.table).get()
        return data, error

    def list(self, handler):
        data, error = Controller(handler=handler, table=self.table).list()
        return data, error

    def add(self, handler):
        data, error = Controller(handler=handler, table=self.table).add()
        return data, error

    def update(self):
        return {}, None

    def remove(self):
        return {}, None

    def count(self):
        return {}, None

    def search(self):
        return {}, None
