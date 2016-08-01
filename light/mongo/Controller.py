from light.mongo.model import Model


class Controller(object):
    """
    1. 封装model的调用, 接收的参数为handler对象
    2. 进行缺省值的设定, 如 updateBy createAt valid 等
    3. 格式化输出的JSON结果, 获取List时会付上件数totalItems等信息
    4. 统一封装关于数据库操作的错误内容
    """

    def __init__(self, handler, table):
        define = {}
        self.model = Model(domain=handler.domain, code=handler.code, table=table, define=define)

        pass


