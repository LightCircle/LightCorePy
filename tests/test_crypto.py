import unittest

from light.crypto import Crypto


class TestCrypto(unittest.TestCase):
    def test_sha256(self):
        sha256 = Crypto.sha256('1qaz2wsx', 'light')
        self.assertEqual(sha256, '1f7f77b31ee95f1ac079b9f99f77684e7c9b900ba9cc4ea8d94c6d9d0c49c8ea')

    def test_encrypt(self):
        result = Crypto.encrypt('2e35501c2b7e', 'light')
        self.assertEqual('d654b787987267137e92e49d170cf24c', result)

    def test_encrypt2(self):
        result = Crypto.encrypt2('2e35501c2b7e', 'light')
        self.assertEqual('SPvPSa3cTKdfLgE7hKh0Pw==', result)

    def test_decrypt(self):
        result = Crypto.decrypt('d654b787987267137e92e49d170cf24c', 'light')
        self.assertEqual('2e35501c2b7e', result)

    def test_decrypt2(self):
        result = Crypto.decrypt2('SPvPSa3cTKdfLgE7hKh0Pw==', 'light')
        self.assertEqual('2e35501c2b7e', result)

    def test_full_space(self):
        self.assertEqual('1               ', Crypto.full_space('1'))
        self.assertEqual('0123456789012345', Crypto.full_space('0123456789012345'))
        self.assertEqual('01234567890123456               ', Crypto.full_space('01234567890123456'))

    def test_jwt_encode(self):
        token = Crypto.jwt_encode({'sid': 'abc'}, 'light', 10)
        decoded = Crypto.jwt_decode(token, 'light')

        self.assertEqual('abc', decoded['sid'])
        self.assertIsNotNone(decoded['expires'])

    def test_jwt_decode(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzIjoxNDgyMTE3MDg4LCJzaWQiOiJhYmMifQ.gh-' \
                '9vnt2rccgpj4DfCNqrYluQjxsv_gmIoBP8eTjI78'
        decoded = Crypto.jwt_decode(token, 'light')
        self.assertEqual('abc', decoded['sid'])
        self.assertIsNotNone(decoded['expires'])

        token = 'bad token value'
        decoded = Crypto.jwt_decode(token, 'light')
        self.assertEqual({}, decoded)
