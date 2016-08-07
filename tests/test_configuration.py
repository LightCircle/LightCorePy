import os
import unittest
from light.cache import Cache
from light.configuration import Config
from light.constant import Const

CONST = Const()


class TestConfig(unittest.TestCase):
    def setUp(self):
        os.environ[CONST.ENV_LIGHT_DB_HOST] = 'db.alphabets.cn'
        os.environ[CONST.ENV_LIGHT_DB_PORT] = '57017'
        os.environ[CONST.ENV_LIGHT_DB_USER] = 'light'
        os.environ[CONST.ENV_LIGHT_DB_PASS] = '2e35501c2b7e'
        Cache(CONST.SYSTEM_DB).init()

    def test_init(self):
        conf = Config()

        self.assertEqual(conf.app.cookieSecret, 'light')
        self.assertTrue(isinstance(conf.ignore.auth, list))
        self.assertTrue(isinstance(conf.mail.auth.user, str))
