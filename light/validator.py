import jmespath

from light.mongo.model import Model
from light.constant import Const

CONST = Const()


class Validator(object):
    def __init__(self, handler):
        self.handler = handler

    def is_valid(self, check, validation=None):
        method = [item for item in validation if item['name'] == check[0]]
        if len(method) <= 0:
            return

        rule = method[0]['rule']
        data = jmespath.search(method[0]['key'], {'data': self.handler.params.data})
        option = method[0]['option']

        result = getattr(Rule(), rule)(self.handler, data, option)
        if not result:
            return method[0]['message']


class Rule(object):
    def __init__(self):
        pass

    @staticmethod
    def is_number(handler, data, option):
        print(data)

        if isinstance(data, int):
            return True

        if isinstance(data, float):
            return True

        return False

    @staticmethod
    def is_string(handler, data, option):
        if isinstance(data, str):
            return True

        return False

    @staticmethod
    def is_unique(handler, data, option):
        model = Model(domain=handler.domain, code=handler.code, table=option['table'])
        count = model.total(condition=option['condition'])
        return count <= 0
