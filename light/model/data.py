from light.constant import Const
from light.mongo.controller import Controller

CONST = Const()


class Data(object):
    def __init__(self, board):
        self.board = board

    def get(self, handler):
        ctrl = Controller(handler=handler, table=self.board['class'])
        return ctrl.get()

    def list(self, handler):
        ctrl = Controller(handler=handler, table=self.board['class'])
        return ctrl.list()

    def add(self):
        return {}

    def update(self):
        return {}

    def remove(self):
        return {}

    def count(self):
        return {}

    def search(self):
        return {}
