import jmespath


class Validator(object):
    def __init__(self, handler):
        self.handler = handler

    def is_valid(self, check, validation=None):
        method = [item for item in validation if item['name'] == check[0]]
        if len(method) <= 0:
            return

        rule = method[0]['rule']
        data = jmespath.search(method[0]['key'], {'data': self.handler.params.data})

        result = getattr(Rule(), rule)(data)
        if not result:
            return method[0]['message']


class Rule(object):
    def __init__(self):
        pass

    @staticmethod
    def is_number(data):
        print(data)

        if isinstance(data, int):
            return True

        if isinstance(data, float):
            return True

        return False

    @staticmethod
    def is_string(data):
        if isinstance(data, str):
            return True

        return False
