import os
import unittest
from light.cache import LRUCache, Cache
from light.constant import Const

CONST = Const()


class TestCache(unittest.TestCase):
    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'db.alphabets.cn'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'

    def test_init(self):
        Cache(CONST.SYSTEM_DB).init()
        self.assertIsNotNone(Cache.instance().get(CONST.SYSTEM_DB_CONFIG))


class TestLURCache(unittest.TestCase):
    def test_cache(self):
        cache = LRUCache(3)
        cache.set('1', 1)
        cache.set('2', 2)
        cache.set('3', 3)
        cache.set('4', 4)

        self.assertEqual(cache.get('1'), -1)
        self.assertEqual(cache.get('2'), 2)
        self.assertEqual(cache.get('3'), 3)
        self.assertEqual(cache.get('4'), 4)
