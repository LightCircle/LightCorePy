import os
import importlib.util


def resolve(name):
    path = os.path.join(os.path.abspath('..'), 'controllers', name + '.py')

    if not os.path.isfile(path):
        return None

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
