from flask import Flask
from functools import partial
import importlib.util
import os

app = Flask(__name__)


# Load python module from file
def loader(name):
    path = os.path.join(os.path.abspath('..'), 'controllers', name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ctrl = loader('hello')
func1 = partial(ctrl.hello, page='hello')
func2 = partial(ctrl.static)
func3 = partial(ctrl.test, page='hello')
func4 = partial(ctrl.upload)


# 绑定URL与CTRL的方法
def bind():
    app.add_url_rule('/{0}'.format('hello'), endpoint='hello', view_func=func1, methods=['GET'])
    app.add_url_rule('/upload', endpoint='mmm', view_func=func3, methods=['GET'])
    app.add_url_rule('/upload', endpoint='nnn', view_func=func4, methods=['POST'])


# 静态资源解析
def bind_static():
    app.add_url_rule('/js/<path:path>', endpoint='sss', view_func=func2)


if __name__ == "__main__":
    bind()
    bind_static()
    app.run()
