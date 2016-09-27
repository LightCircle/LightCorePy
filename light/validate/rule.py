"""
rule.py
"""


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

    #@staticmethod
    #def range(data, start, end, inclusive=True):
    #    if inclusive:
    #        return start <= data <= end
    #    else:
    #        return start < data < end

    # create new ...