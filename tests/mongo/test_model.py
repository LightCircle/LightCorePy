import os
import unittest
from light.mongo.model import Model


class TestModel(unittest.TestCase):
    def setUp(self):
        os.environ['LIGHTDB_HOST'] = 'localhost'
        os.environ['LIGHTDB_PORT'] = '1'

    def test_add(self):
        Model('python', 'aaa', 'test').add()

    def tearDown(self):
        pass
