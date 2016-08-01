import os
import unittest
from light.cache import LRUCache, Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        os.environ['LIGHTDB_HOST'] = 'db.alphabets.cn'
        os.environ['LIGHTDB_PORT'] = '57017'
        os.environ['LIGHTDB_USER'] = 'light'
        os.environ['LIGHTDB_PASS'] = '2e35501c2b7e'

    def test_init(self):
        Cache('LightDB').init()
        self.assertIsNotNone(Cache.instance().get('configuration'))


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
