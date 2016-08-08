import os
import importlib.util


def resolve(name, path=''):
    path = os.path.join(path, name + '.py')
    print(path)
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
