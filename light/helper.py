import os
import re
import string
import random
import jinja2
import importlib.util


def resolve(name, path=''):
    path = os.path.join(path, name + '.py')

    if not os.path.isfile(path):
        return None

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def project_path(*relate):
    path = os.getcwd()

    if relate:
        return os.path.join(path, *relate)

    return path


def core_path(*relate):
    path = os.path.dirname(os.path.abspath(__file__))

    if relate:
        return os.path.join(path, *relate)

    return path


def load_template(name, path=None):
    if not path:
        path = project_path('views')

    loader = jinja2.FileSystemLoader(path, 'utf-8')

    environment = jinja2.Environment(
        loader=loader,
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<%=',
        variable_end_string='%>')

    return environment.get_template(name + '.html')


def random_guid(size=4, upper=False):
    base = string.ascii_lowercase + string.digits
    if upper:
        base = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(base) for _ in range(size))


def is_mobile(headers):
    ua = headers['user-agent'] or ''

    is_apple = re.match('iPhone', ua) or re.match('', ua) or re.match('', ua)
    if is_apple:
        return True

    is_android = re.match('(?=.*\bAndroid\b)(?=.*\bMobile\b)', ua) or re.match('Android', ua)
    if is_android:
        return True

    is_windows = re.match('IEMobile', ua) or re.match('(?=.*\bWindows\b)(?=.*\bARM\b)', ua)
    if is_windows:
        return True

    return False


def is_browser(headers):
    ua = headers['user-agent'] or ''
    return re.match('mozilla.*', ua.lower())
