import hmac
import hashlib
import binascii
import math
import jwt

from Crypto.Cipher import AES
from datetime import datetime, timedelta


class Crypto(object):
    @staticmethod
    def sha256(message, secret):
        secret = bytes(secret, 'ascii')
        message = bytes(message, 'ascii')

        return hmac.new(secret, message, hashlib.sha256).hexdigest()

    @staticmethod
    def encrypt(message, secret):
        message = Crypto.full_space(message)
        secret = Crypto.full_space(secret)

        cipher = AES.new(secret, AES.MODE_ECB)
        return str(binascii.b2a_hex(cipher.encrypt(message)), 'utf8')

    @staticmethod
    def decrypt(message, secret):
        message = Crypto.full_space(message)
        secret = Crypto.full_space(secret)

        decipher = AES.new(secret, AES.MODE_ECB)
        return str(decipher.decrypt(binascii.a2b_hex(message)).rstrip(), 'utf8')

    @staticmethod
    def full_space(string):
        decimal, integer = math.modf(len(string) / 16)
        if decimal == 0:
            return string

        return string + ' ' * ((int(integer) + 1) * 16 - len(string))

    @staticmethod
    def jwt_encode(payload, secret, expires):
        time = datetime.now() + timedelta(seconds=expires)
        payload['expires'] = int(time.timestamp())
        return jwt.encode(payload, secret, algorithm='HS256').decode(encoding='UTF-8')

    @staticmethod
    def jwt_decode(token, secret):
        try:
            return jwt.decode(token.encode(encoding='UTF-8'), secret, algorithms=['HS256'])
        except:
            return {}
