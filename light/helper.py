import os
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
