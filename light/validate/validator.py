"""
validator.py
"""

import jmespath

from light.validate.rule import *
from light.validate.define import Items


class Validator(object):
    def __init__(self, handler):
        self.handler = handler

    def is_valid(self, check, validation=None):
        if not isinstance(validation, Items):
            return

        method = validation.get(check)
        if len(method) <= 0:
            return

        # result <- list?
        for validator in method:
            rule = validator.rule
            data = jmespath.search(validator.key, {'data': self.handler.params.data})

            if validator.option is None:
                result = getattr(Rule(), rule)(data)
            else:
                result = getattr(Rule(), rule)(data, validator.option)
            if not result:
                return validator.message
