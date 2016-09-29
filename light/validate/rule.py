"""
rule.py
"""

import json

from datetime import datetime, date


class Rule(object):
    def __init__(self):
        pass

    @staticmethod
    def is_number(data):
        return isinstance(data, int) or isinstance(data, float)

    @staticmethod
    def is_string(data):
        return isinstance(data, str)

    @staticmethod
    def range(data, option, inclusive=True):
        min_len, max_len = [int(x) for x in option]
        if inclusive:
            return min_len <= len(data) <= max_len
        else:
            return min_len < len(data) < max_len

    @staticmethod
    def is_boolean(data):
        return isinstance(data, bool)

    @staticmethod
    def is_date(data):
        return isinstance(data, date) or isinstance(data, datetime)

    @staticmethod
    def is_array(data):
        return isinstance(data, (list, tuple))

    @staticmethod
    def equals(data, option):
        return data == option

    @staticmethod
    def gt(data, option):
        return data > option

    @staticmethod
    def gte(data, option):
        return data >= option

    @staticmethod
    def lt(data, option):
        return data < option

    @staticmethod
    def lte(data, option):
        return data <= option

    @staticmethod
    def is_json(data):
        try:
            json.loads(data)
        except ValueError:
            return False

        return True

    @staticmethod
    def contains(data, option):
        return data in option

    @staticmethod
    def is_empty(data):
        return data is None