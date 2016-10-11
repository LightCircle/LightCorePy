"""
rule.py
"""

import json
import re
import jmespath

from datetime import datetime, date
from light.mongo.model import Model

"""
email Regular Expression
"""
email_user_regex = re.compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+"
    r"(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|'
    r"""\\[\001-\011\013\014\016-\177])*"$)""",
    re.IGNORECASE
)
email_domain_regex = re.compile(
    # domain
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?$)'
    # literal form, ipv4 address (SMTP 4.1.3)
    r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)'
    r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE)


"""
url Regular Expression
"""
url_ip_middle_octet = u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
url_ip_last_octet = u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
url_regex = re.compile(
    u"^"
    # protocol identifier
    u"(?:(?:https?|ftp)://)"
    # user:pass authentication
    u"(?:\S+(?::\S*)?@)?"
    u"(?:"
    u"(?P<private_ip>"
    # IP address exclusion
    # private & local networks
    u"(?:(?:10|127)" + url_ip_middle_octet + u"{2}" + url_ip_last_octet + u")|"
    u"(?:(?:169\.254|192\.168)" + url_ip_middle_octet + url_ip_last_octet + u")|"
    u"(?:172\.(?:1[6-9]|2\d|3[0-1])" + url_ip_middle_octet + url_ip_last_octet + u"))"
    u"|"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    u"(?P<public_ip>"
    u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    u"" + url_ip_middle_octet + u"{2}"
    u"" + url_ip_last_octet + u")"
    u"|"
    # host name
    u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    u")"
    # port number
    u"(?::\d{2,5})?"
    # resource path
    u"(?:/\S*)?"
    u"$",
    re.UNICODE | re.IGNORECASE
)


class Rule(object):
    def __init__(self):
        pass

    @staticmethod
    def is_number(handler, data, option):
        return isinstance(data, int) or isinstance(data, float)

    @staticmethod
    def is_string(handler, data, option):
        return isinstance(data, str)

    @staticmethod
    def range(handler, data, option):
        min_len, max_len = [int(x) for x in option]
        return min_len <= len(data) <= max_len

    @staticmethod
    def is_boolean(handler, data, option):
        return isinstance(data, bool)

    @staticmethod
    def is_date(handler, data, option):
        return isinstance(data, date) or isinstance(data, datetime)

    @staticmethod
    def is_array(handler, data, option):
        return isinstance(data, (list, tuple))

    @staticmethod
    def equals(handler, data, option):
        return data == option

    @staticmethod
    def gt(handler, data, option):
        return data > option

    @staticmethod
    def gte(handler, data, option):
        return data >= option

    @staticmethod
    def lt(handler, data, option):
        return data < option

    @staticmethod
    def lte(handler, data, option):
        return data <= option

    @staticmethod
    def is_json(handler, data, option):
        if not isinstance(data, str):
            return False

        try:
            json.loads(data)
        except ValueError:
            return False

        return True

    @staticmethod
    def contains(handler, data, option):
        return data in option

    @staticmethod
    def is_empty(handler, data, option):
        return data is None

    @staticmethod
    def is_email(handler, data, option):
        if not data or '@' not in data:
            return False

        user_part, domain_part = data.rsplit('@', 1)
        if not email_user_regex.match(user_part) or not email_domain_regex.match(domain_part):
            return False

        return True

    @staticmethod
    def is_url(handler, data, option):
        if not url_regex.match(data):
            return False

        return True

    @staticmethod
    def is_ip(handler, data, option):
        if int(option) == 4:
            parts = data.split('.')
            if len(parts) == 4 and all(x.isdigit() for x in parts):
                numbers = list(int(x) for x in parts)
                return all(0 <= num < 256 for num in numbers)
        elif int(option) == 6:
            parts = data.split(':')
            if len(parts) > 8:
                return False

            num_blank = 0
            for part in parts:
                if not part:
                    num_blank += 1
                else:
                    try:
                        value = int(part, 16)
                    except ValueError:
                        return False
                    else:
                        if value < 0 or value >= 65536:
                            return False

            if num_blank < 2:
                return True
            elif num_blank == 2 and not parts[0] and not parts[1]:
                return True

        return False

    @staticmethod
    def is_unique(handler, data, option):
        model = Model(domain=handler.domain, code=handler.code, table=option['table'])
        for key, val in option['condition'].items():
            if isinstance(val, str) and val.count('$') == 1:
                option['condition'][key] = jmespath.search(val.replace('$', ''), {'data': handler.params.data})
        count = model.total(condition=option['condition'])
        return count <= 0

    @staticmethod
    def is_exists(handler, data, option):
        model = Model(domain=handler.domain, code=handler.code, table=option['table'])
        for key, val in option['condition'].items():
            if isinstance(val, str) and val.count('$') == 1:
                condition_data = jmespath.search(val.replace('$', ''), {'data': handler.params.data})
                if not isinstance(condition_data, list):
                    condition_data = list(condition_data)
                option['condition'][key] = {'$in': condition_data}
        count = model.total(condition=option['condition'])
        return count > 0
