"""
rule.py
"""

import json
import re
import jmespath
import dateutil.parser
import math

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
        return isinstance(data, (int, float))

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
        return isinstance(data, (date, datetime))

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
        blank_regex = re.compile(r'^(?:\s*)$')
        naninf_regex = re.compile(r'(^(?:[-+])?(?:[N,n])(?:[A,a])(?:[N,n])$)|(^(?:[-+])?(?:[I,i])(?:[N,n])(?:[F,f])$)')
        if not data:
            return True
        elif isinstance(data, str) and blank_regex.match(data):
            return True
        elif isinstance(data, float) \
                and (math.isnan(data) or math.isinf(data)):
            return True
        elif isinstance(data, str) and naninf_regex.match(data) \
                and (math.isnan(float(data)) or math.isinf(float(data))):
            return True

        return False

    @staticmethod
    def is_required(handler, data, option):
        return not Rule.is_empty(handler, data, option)

    @staticmethod
    def is_email(handler, data, option):
        if not isinstance(data, str):
            return False

        if not data or '@' not in data:
            return False

        user_part, domain_part = data.rsplit('@', 1)
        if not email_user_regex.match(user_part) or not email_domain_regex.match(domain_part):
            return False

        return True

    @staticmethod
    def is_url(handler, data, option):
        if not isinstance(data, str):
            return False

        if not url_regex.match(data):
            return False

        return True

    @staticmethod
    def is_ip(handler, data, option):
        if not isinstance(data, str):
            return False

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
            if isinstance(val, str) and val.startswith('$'):
                option['condition'][key] = jmespath.search(val.replace('$', ''), {'data': handler.params.data})
        count = model.total(condition=option['condition'])
        return count <= 0

    @staticmethod
    def is_exists(handler, data, option):
        model = Model(domain=handler.domain, code=handler.code, table=option['table'])
        for key, val in option['condition'].items():
            if isinstance(val, str) and val.startswith('$'):
                condition_data = jmespath.search(val.replace('$', ''), {'data': handler.params.data})
                if not isinstance(condition_data, list):
                    condition_data = list(condition_data)
                option['condition'][key] = {'$in': condition_data}
        count = model.total(condition=option['condition'])
        return count > 0

    @staticmethod
    def to_number(data):
        if not isinstance(data, str):
            return data

        int_regex = re.compile(r'^(?:[-+])?(?:\d+)$')
        number_regex = re.compile(r'^(?:[-+])?((?:\d+)|((?:\d+\.)|(?:\.\d+)|(?:\d+\.\d+)))(?:[eE][\+\-]?(?:\d+))?$')

        if number_regex.match(data):
            if int_regex.match(data):
                return int(data)
            return float(data)

        return data

    @staticmethod
    def to_date(data):
        if not isinstance(data, str):
            return data

        try:
            dateutil.parser.parse(data)
        except ValueError:
            return data

        return dateutil.parser.parse(data)

    @staticmethod
    def to_boolean(data):
        if data == 'true' or data == 'True' or data == '1':
            return True
        if data == 'false' or data == 'False' or data == '0' or data is None:
            return False

        return data

    @staticmethod
    def to_string(data):
        if data is None:
            return ''

        return str(data)

    @staticmethod
    def ltrim(data, chars=''):
        if not isinstance(data, str):
            return data

        pattern = re.compile(r'^[' + chars + ']+') if chars else re.compile(r'^\s+')
        return re.sub(pattern, '', data)

    @staticmethod
    def rtrim(data, chars=''):
        if not isinstance(data, str):
            return data

        pattern = re.compile(r'[' + chars + ']') if chars else re.compile(r'\s')
        idx = len(data) - 1
        for idx in range(len(data) - 1, 0, -1):
            if not pattern.match(data[idx]):
                break

        return data[0:(idx + 1)]

    @staticmethod
    def trim(data, chars=''):
        if not isinstance(data, str):
            return data

        return Rule.rtrim(Rule.ltrim(data, chars), chars)

    @staticmethod
    def escape(data):
        if not isinstance(data, str):
            return data

        return data.replace(r'&', r'&amp;').replace(r'"', r'&quot;').replace(r"'", r'&#x27;').replace(r'<', r'&lt;') \
            .replace(r'>', r'&gt;').replace(r'/', r'&#x2F;').replace(r'`', r'&#96;')

    @staticmethod
    def unescape(data):
        if not isinstance(data, str):
            return data

        return data.replace(r'&amp;', r'&').replace(r'&quot;', r'"').replace(r'&#x27;', r"'").replace(r'&lt;', r'<') \
            .replace(r'&gt;', r'>').replace(r'&#x2F;', r'/').replace(r'&#96;', r'`')
