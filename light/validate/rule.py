"""
rule.py
"""


class Rule(object):
    def __init__(self):
        pass

    @staticmethod
    def is_number(data):
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

    @staticmethod
    def range(data, option, inclusive=True):
        min_len, max_len = [int(x) for x in option]
        if inclusive:
            return min_len <= len(data) <= max_len
        else:
            return min_len < len(data) < max_len