import os
import inflect

from pymongo import MongoClient

SYSTEM_DB = 'LightDB'


class Model:
    def __init__(self, domain, code, table, define=None, user=None, password=None):
        self.domain = domain
        self.code = code
        self.define = define
        self.user = user
        self.password = password

        # Plural form
        self.table = inflect.engine().plural(table)

        # When using the system db, table name without the prefix
        if self.domain == SYSTEM_DB:
            self.code = self.table
        else:
            self.code = self.code + '.' + self.table

        # Environment Variables higher priority
        host = os.getenv('LIGHTDB_HOST', 'db')
        port = os.getenv('LIGHTDB_PORT', 57017)
        user = os.getenv('LIGHTDB_USER', self.user)
        password = os.getenv('LIGHTDB_PASS', self.password)

        # Initialize database connection
        if user is None:
            uri = 'mongodb://{host}:{port}/{db}'
            self.db = MongoClient(uri.format(host=host, port=port, db=self.domain))
        else:
            uri = 'mongodb://{user}:{password}@{host}:{port}/{db}?authSource={db}&authMechanism=MONGODB-CR'
            self.db = MongoClient(uri.format(host=host, port=port, user=user, password=password, db=self.domain))

        print('{domain} / {code}'.format(domain=self.domain, code=self.code))

    def get(self):
        pass

    def get_by(self):
        pass

    def add(self):
        pass

    def update(self):
        pass

    def update_by(self):
        pass

    def remove(self):
        pass

    def remove_by(self):
        pass

    def total(self):
        pass

    def increment(self):
        pass

    def write_file_to_grid(self):
        pass

    def write_buffer_to_grid(self):
        pass

    def write_stream_to_grid(self):
        pass

    def read_file_from_grid(self):
        pass

    def read_buffer_from_grid(self):
        pass

    def read_stream_from_grid(self):
        pass

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
