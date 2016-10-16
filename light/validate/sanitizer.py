"""
sanitizer.py
"""

import jmespath

from light.validate.rule import *
from light.validate.define import Items


class Sanitizer(object):
    def __init__(self, handler):
        self.handler = handler

    def to_valid(self, check, sanitization=None):
        if not isinstance(sanitization, Items):
            return

        method = sanitization.get(check)
        if len(method) <= 0:
            return

        # result <- list?
        for sanitizer in method:
            rule = sanitizer.rule
            data = jmespath.search(sanitizer.key, {'data': self.handler.params.data})

            result = getattr(Rule(), rule)(data)
            return result
