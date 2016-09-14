import os
import re
import inflect
import mimetypes

from pymongo import MongoClient
from bson.objectid import ObjectId
from light.constant import Const
from gridfs import GridFS, GridFSBucket

from light.mongo.mapping import Update, Query
from light.mongo.define import Items

CONST = Const()


class Model:
    """
    1. 创建于数据库的连接, 并保持连接池
    2. 数据库连接信息通过环境变量设定
    3. 用表结构的定义, 对保存的数据进行类型转换
    4. 用表结构的定义, 对条件中的数据进行类型转换
    5. 功能包括: 通常的CURD, GridFS操作, 数据库索引操作, 数据库用户操作
    """

    def __init__(self, domain, code=None, table=None, define=None, user=None, password=None):
        self.domain = domain
        self.code = code
        self.define = define
        self.user = user
        self.password = password
        self.table = table

        if table:
            # Plural form
            self.table = inflect.engine().plural(table)

            # When using the system db, table name without the prefix
            if self.domain == CONST.SYSTEM_DB:
                self.code = self.table
            else:
                self.code = self.code + '.' + self.table

        # Environment Variables higher priority
        host = os.getenv(CONST.ENV_LIGHT_DB_HOST, 'db')
        port = os.getenv(CONST.ENV_LIGHT_DB_PORT, 27017)
        user = os.getenv(CONST.ENV_LIGHT_DB_USER, self.user)
        password = os.getenv(CONST.ENV_LIGHT_DB_PASS, self.password)
        auth = os.getenv(CONST.ENV_LIGHT_DB_AUTH, 'MONGODB-CR')

        # Initialize database connection
        if user is None:
            uri = 'mongodb://{host}:{port}/{db}'
            self.client = MongoClient(uri.format(host=host, port=port, db=self.domain))
        else:
            uri = 'mongodb://{user}:{password}@{host}:{port}/{db}?authSource={db}&authMechanism={auth}'
            self.client = MongoClient(uri.format(
                host=host, port=port, user=user, password=password, db=self.domain, auth=auth))

        self.db = self.client[self.domain]
        if self.code:
            self.db = self.db[self.code]

        print('{domain} / {code}'.format(domain=self.domain, code=self.code))

    def get(self, condition=None, select=None):

        # Convert string or object id to dict
        #if isinstance(condition, str):
        #    condition = {'_id': ObjectId(condition)}
        #elif isinstance(condition, ObjectId):
        #    condition = {'_id': condition}
        #elif isinstance(condition, dict):
        #    Query.parse(condition, Items(self.define))

        if isinstance(condition, dict):
            Query.parse(condition, Items(self.define))
        else:
            if isinstance(condition, ObjectId):
                condition = {'_id': condition}
            else:
                condition = {'_id': ObjectId(str(condition))}


        Query.parse(select, Items(self.define))

        return self.db.find_one(filter=condition, projection=select)

    def get_by(self, condition=None, select=None):

        # Convert string to dict : a,b,c -> {'a': 1, 'b': 1, 'c': 1}
        if isinstance(select, str):
            select = re.split(r'[, ]', select)
            select = {select[i]: 1 for i in range(0, len(select))}

        Query.parse(condition, Items(self.define))
        Query.parse(select, Items(self.define))

        return list(self.db.find(filter=condition, projection=select))

    def add(self, data=None):

        Update.parse(data, Items(self.define))

        data = self.db.insert_one(data)
        return data.inserted_id

    def update(self, condition = None, update = None):

        #if isinstance(condition, str):
        #    condition = {'_id': ObjectId(condition)}
        #elif isinstance(condition, ObjectId):
        #    condition = {'_id': condition}
        #elif isinstance(condition, dict):
        #    Query.parse(condition, Items(self.define))

        if isinstance(condition, dict):
            Query.parse(condition, Items(self.define))
        else:
            if isinstance(condition, ObjectId):
                condition = {'_id': condition}
            else:
                condition = {'_id': ObjectId(str(condition))}

        Update.parse(update, Items(self.define))

        return self.db.update_one(filter=condition, update=update)

    def update_by(self, condition = None, update = None):

        Query.parse(condition, Items(self.define))
        Update.parse(update, Items(self.define))

        return self.db.update_many(filter=condition, update=update)

    def remove(self, condition = None):
        pass
        #Update.parse(condition, Items(self.define))
        #return self.db.delete_one(condition)

    def remove_by(self, condition = None):
        pass
        #Update.parse(condition, Items(self.define))
        #return self.db.delete_many(condition)

    def total(self, condition):

        Query.parse(condition, Items(self.define))

        return self.db.count(filter=condition)

    def increment(self, condition = None, update = None):

        #if isinstance(condition, str):
        #    condition = {'_id': ObjectId(condition)}
        #elif isinstance(condition, ObjectId):
        #    condition = {'_id': condition}
        #elif isinstance(condition, dict):
        #    Query.parse(condition, Items(self.define))

        if isinstance(condition, dict):
            Query.parse(condition, Items(self.define))
        else:
            if isinstance(condition, ObjectId):
                condition = {'_id': condition}
            else:
                condition = {'_id': ObjectId(str(condition))}

        Update.parse(update, Items(self.define))

        return self.db.find_one_and_update(filter=condition, update=update)

    def write_file_to_grid(self, file):
        grid = GridFS(self.db)
        f = open(file, 'rb')

        content_type, encoding = mimetypes.guess_type(file)
        filename = os.path.basename(f.name)

        result = {
            'name': filename,
            'contentType': content_type,
            'length': os.path.getsize(file),
            'fileId': grid.put(f.read(), filename=filename, content_type=content_type)
        }

        f.close()
        return result

    def write_buffer_to_grid(self):
        raise NotImplementedError

    def write_stream_to_grid(self, name, stream, content_type):
        return {
            'name': name,
            'contentType': content_type,
            'length': 0,
            'fileId': GridFSBucket(self.db).upload_from_stream(name, stream, metadata={'contentType': content_type})
        }

    def read_file_from_grid(self, fid, file):
        if isinstance(fid, str):
            fid = ObjectId(fid)

        grid = GridFS(self.db).get(fid)

        f = open(file, 'wb')
        f.write(grid.read())
        f.close()

        return {
            'name': grid.filename,
            'contentType': grid.content_type,
            'length': grid.chunk_size,
            'fileId': fid,
            'uploadDate': grid.upload_date
        }

    def read_buffer_from_grid(self):
        raise NotImplementedError

    def read_stream_from_grid(self, fid):
        if isinstance(fid, str):
            fid = ObjectId(fid)

        grid = GridFSBucket(self.db).open_download_stream(fid)
        return {
            'name': grid.filename,
            'contentType': grid.content_type,
            'length': grid.chunk_size,
            'fileId': fid,
            'uploadDate': grid.upload_date,
            'fileStream': grid.read()
        }

    def create_user(self):
        pass

    def add_user(self):
        pass

    def drop_user(self):
        pass

    def change_password(self):
        pass

    def drop_database(self):
        pass
