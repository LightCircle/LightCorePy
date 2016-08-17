from light.mongo.type import *
from light.mongo.define import Items
from light.mongo.operator import UpdateOperator, QueryOperator

"""
mapping: 根据数据库字段的定义, 对数据进行类型转换 (包括两种类型的数据: 1.跟新用的数据本身, 2.检索条件中的数据)
define: 具体字段的定义, 为了代码中使用方便, 变成了类的形式
operator: 处理Mongodb的操作符, 基于 ver3.2 的文档进行操作
type: 负责实际的数据类型转换, 当输入数据为 dict 或 list 时, 进行递归转换
"""


class Update(object):
    @staticmethod
    def parse(data, defines):
        if isinstance(data, dict):
            data = [data]

        for datum in data:
            for key, val in datum.items():
                define = defines.get(key)

                # Parse sub items
                if define is not None and isinstance(define.contents, Items):
                    Update.parse(val, define.contents)
                    continue

                # If the key contains mongodb operator, ex. {$set: {field: val}}
                if key.startswith('$'):
                    UpdateOperator().parse(key, val, defines)
                    continue

                # If define not found, then parse next
                if define is None:
                    continue

                # Is array basic type
                if isinstance(val, list):
                    datum[key] = globals()[define.contents].parse(val)

                # Parse basic type
                else:
                    datum[key] = globals()[define.type].parse(val)


class Query(object):
    @staticmethod
    def parse(data, defines):

        for key, val in data.items():

            # If the key contains mongodb operator, ex. {$set: {field: val}}
            if key.startswith('$'):
                QueryOperator().parse(key, val, defines)
                continue

            define = defines.get(key)

            # If define not found, then parse next
            if define is None:
                continue

            data[key] = globals()[define.type].parse(val)
