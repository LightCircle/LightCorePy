import os
import unittest
from light.cache import Cache
from light.configuration import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        os.environ['LIGHTDB_HOST'] = 'db.alphabets.cn'
        os.environ['LIGHTDB_PORT'] = '57017'
        os.environ['LIGHTDB_USER'] = 'light'
        os.environ['LIGHTDB_PASS'] = '2e35501c2b7e'
        Cache('LightDB').init()

    def test_init(self):
        conf = Config()

        self.assertEqual(conf.app.cookieSecret, 'light')
        self.assertTrue(isinstance(conf.ignore.auth, list))
        self.assertTrue(isinstance(conf.mail.auth.user, str))
