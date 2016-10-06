import os
import light.helper
from datetime import datetime

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

        self.uid = handler.uid
        self.model = Model(domain=handler.domain, code=handler.code, table=table, define=define)
        self.condition = handler.params.condition or {}
        self.data = handler.params.data or {}
        self.id = handler.params.id
        self.select = handler.params.select or handler.params.field
        self.sort = handler.params.sort
        self.files = handler.params.files
        self.skip = handler.params.skip
        self.limit = handler.params.limit or 100

        if self.skip is None:
            self.skip = 0

    def get(self):
        if 'valid' not in self.condition:
            self.condition['valid'] = CONST.VALID

        result = self.model.get(condition=self.id or self.condition, select=self.select)
        return result, None

    def list(self):
        if 'valid' not in self.condition:
            self.condition['valid'] = CONST.VALID

        count = self.model.total(condition=self.condition)
        result = self.model.get_by(
            condition=self.condition, select=self.select, sort=self.sort, skip=self.skip, limit=self.limit
        )
        return {'totalItems': count, 'items': result}, None

    def add(self):
        if not isinstance(self.data, list):
            self.data = [self.data]

        for data in self.data:
            regular = {
                'createAt': datetime.now(),
                'createBy': self.uid,
                'updateAt': datetime.now(),
                'updateBy': self.uid,
                'valid': CONST.VALID
            }
            data.update(regular)

        result = self.model.add(data=self.data)
        return {'_id': result}, None

    def total(self):
        if 'valid' not in self.condition:
            self.condition['valid'] = CONST.VALID

        count = self.model.total(condition=self.condition)
        return count, None

    def count(self):
        return self.total()

    def update(self, upsert=False):
        if 'valid' not in self.condition:
            self.condition['valid'] = CONST.VALID

        regular = {'updateAt': datetime.now(), 'updateBy': self.uid}
        self.data.update(regular)

        # If the update operation does not result in an insert, $setOnInsert does nothing.
        data = {
            '$set': self.data,
            '$setOnInsert': {'createAt': datetime.now(), 'createBy': self.uid, 'valid': CONST.VALID}
        }

        result = self.model.update_by(condition=self.id or self.condition, data=data, upsert=upsert)
        return {'_id': result}, None

    def increment(self, upsert=True):
        regular = {'updateAt': datetime.now(), 'updateBy': self.uid}
        self.data.update(regular)

        data = {'$inc': self.data}
        result = self.model.increment(condition=self.id or self.condition, update=data, upsert=upsert)
        return result, None

    def remove(self):
        regular = {'updateAt': datetime.now(), 'updateBy': self.uid, 'valid': CONST.INVALID}
        result = self.model.update_by(condition=self.id or self.condition, data={'$set': regular})
        return {'_id': result}, None

    def delete(self):
        result = self.model.remove_by(condition=self.id or self.condition)
        return result, None

    def distinct(self):
        result = self.model.distinct(key=self.select, filter=self.condition)
        return result, None

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
