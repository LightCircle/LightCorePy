import os
import unittest
from light.mongo.model import Model
from light.constant import Const

CONST = Const()


class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'localhost'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

    def setUp(self):
        pass

    def test_add(self):
        model = Model('LightDB', 'light', 'unittest')
        a = model.add({'a': 'a', 'b': 1})
        print(a)

    def test_get(self):
        model = Model('LightDB', 'light', 'unittest')
        model.get()

    def test_get_by(self):
        model = Model('LightDB', 'light', 'unittest')
        pa = model.get_by()
        print(pa)

    def test_total(self):
        model = Model('LightDB', 'light', 'unittest')
        self.assertGreater(model.total({'b': 1}), 1)

    def test_write_file_to_grid(self):
        in_file = 'test_model.py'
        out_file = in_file + '.temp'
        model = Model('LightDB')

        result = model.write_file_to_grid(in_file)

        result = model.read_file_from_grid(result['fileId'], out_file)
        self.assertEqual(in_file, result['name'])
        self.assertTrue(os.path.isfile(out_file))
        os.remove(out_file)

    def test_write_stream_to_grid(self):
        in_file = 'test_model.py'
        out_file = in_file + '.temp'

        model = Model('LightDB')

        f = open(in_file, 'rb')
        result = model.write_stream_to_grid(in_file, f, 'text/x-python')
        f.close()

        result = model.read_stream_from_grid(result['fileId'])
        f = open(out_file, 'wb')
        f.write(result['fileStream'])
        f.close()

        self.assertEqual(in_file, result['name'])
        self.assertTrue(os.path.isfile(out_file))
        os.remove(out_file)
