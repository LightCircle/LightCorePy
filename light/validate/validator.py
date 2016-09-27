"""
validator.py
"""

import jmespath

from light.validate.rule import *


class Validator(object):
    def __init__(self, handler):
        self.handler = handler

    def is_valid(self, check, validation=None):
        method = validation.get(check)
        if len(method) <= 0:
            return

        for validator in method:
            rule = validator.rule
            data = jmespath.search(validator.key, {'data': self.handler.params.data})

            result = getattr(Rule(), rule)(data)
            if not result:
                return validator.message