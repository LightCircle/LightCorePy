import os
import light.helper

from light.mongo.model import Model
from light.constant import Const
from light.model.structure import Structure
from light.configuration import Config

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
        self.id = handler.params.id
        self.select = handler.params.select
        self.data = handler.params.data
        self.files = handler.params.files

    def get(self):
        if self.id:
            condition = self.id
        else:
            condition = self.condition

        data = self.model.get(condition=condition, select=self.select)
        return data, None

    def list(self):
        count = self.model.total(condition=self.condition)
        data = self.model.get_by(condition=self.condition, select=self.select)
        return {'totalItems': count, 'items': data}, None

    def add(self):
        data = self.model.add(data=self.data)
        return {'_id': data}, None

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

    def write_file_to_grid(self):
        data = []
        for file in self.files:
            data.append(self.model.write_file_to_grid(file))

        return {'totalItems': len(self.files), 'items': data}, None

    def write_buffer_to_grid(self):
        raise NotImplementedError

    def write_stream_to_grid(self):
        data = []
        for file in self.files:
            content_type = file.content_type
            name = file.filename
            data.append(self.model.write_stream_to_grid(name, file.stream(), content_type))

        return {'totalItems': len(self.files), 'items': data}, None

    def read_file_from_grid(self):
        folder = self.data['folder']
        name = self.data['name']
        if folder is None:
            folder = Config.instance().app.tmp
        if name is None:
            name = light.helper.random_guid(8)

        return self.model.read_file_from_grid(self.id, os.path.join(folder, name))

    def read_buffer_from_grid(self):
        raise NotImplementedError

    def read_stream_from_grid(self):
        return self.model.read_stream_from_grid(self.id)
