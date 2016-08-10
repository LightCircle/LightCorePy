from light.mongo.model import Model
from light.constant import Const
from light.model.structure import Structure

CONST = Const()


class Controller(object):
    """
    1. 封装model的调用, 接收的参数为handler对象
    2. 进行缺省值的设定, 如 updateBy createAt valid 等
    3. 格式化输出的JSON结果, 获取List时会付上件数totalItems等信息
    4. 统一封装关于数据库操作的错误内容
    """

    def __init__(self, handler, table=None):
        define = {}
        if table:
            define = getattr(Structure.instance(), table)['items']

        self.model = Model(domain=handler.domain, code=handler.code, table=table, define=define)
        self.condition = handler.params.condition
        self.select = handler.params.select

    def list(self):
        return self.model.get_by(condition=self.condition, select=self.select)

    def create_user(self):
        raise NotImplementedError

    def add_user(self):
        raise NotImplementedError

    def drop_user(self):
        raise NotImplementedError

    def change_password(self):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def aggregate(self):
        raise NotImplementedError

    def increment(self):
        raise NotImplementedError
