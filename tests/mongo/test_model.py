import os
import unittest
from light.mongo.model import Model


class TestModel(unittest.TestCase):
    def setUp(self):
        os.environ['LIGHTDB_HOST'] = 'localhost'
        os.environ['LIGHTDB_PORT'] = '57017'

    def test_add(self):
        model = Model('python', 'light', 'test')
        model.add({'a': 'a', 'b': 1})

    def test_get(self):
        model = Model('python', 'light', 'test')
        model.get()

    def test_get_by(self):
        model = Model('python', 'light', 'test')
        pa = model.get_by()
        print(pa)

    def tearDown(self):
        pass
