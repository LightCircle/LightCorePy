import unittest

from light.crypto import Crypto


class TestCrypto(unittest.TestCase):
    def test_sha256(self):
        sha256 = Crypto.sha256('1qaz2wsx', 'light')
        self.assertEqual(sha256, '1f7f77b31ee95f1ac079b9f99f77684e7c9b900ba9cc4ea8d94c6d9d0c49c8ea')

    def test_encrypt(self):
        result = Crypto.encrypt('2e35501c2b7e', 'light')
        self.assertEqual('d654b787987267137e92e49d170cf24c', result)

    def test_decrypt(self):
        result = Crypto.decrypt('d654b787987267137e92e49d170cf24c', 'light')
        self.assertEqual('2e35501c2b7e', result)

    def test_full_space(self):
        self.assertEqual('1               ', Crypto.full_space('1'))
        self.assertEqual('0123456789012345', Crypto.full_space('0123456789012345'))
        self.assertEqual('01234567890123456               ',
                         Crypto.full_space('01234567890123456'))
