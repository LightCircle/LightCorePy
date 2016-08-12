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
