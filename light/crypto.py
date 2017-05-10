import hmac
import hashlib
import binascii
import math
import jwt
import base64

from Crypto.Cipher import AES
from hashlib import md5
from datetime import datetime, timedelta

BLOCK_SIZE = 16


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
    def encrypt2(message, secret):

        def pad(d):
            p = BLOCK_SIZE - len(d) % BLOCK_SIZE
            return d + p * chr(p)

        m = md5()
        m.update(secret.encode('utf-8'))
        key = m.hexdigest()

        m = md5()
        m.update((secret + key).encode('utf-8'))
        iv = m.hexdigest()

        data = pad(message)

        aes = AES.new(key, AES.MODE_CBC, iv[:16])

        encrypted = aes.encrypt(data)
        return str(base64.urlsafe_b64encode(encrypted), 'utf8')

    @staticmethod
    def decrypt(message, secret):
        message = Crypto.full_space(message)
        secret = Crypto.full_space(secret)

        decipher = AES.new(secret, AES.MODE_ECB)
        return str(decipher.decrypt(binascii.a2b_hex(message)).rstrip(), 'utf8')

    @staticmethod
    def decrypt2(message, secret):

        def un_pad(padded):
            pad = ord(chr(padded[-1]))
            return padded[:-pad]

        encoded = base64.urlsafe_b64decode(message)

        m = md5()
        m.update(secret.encode('utf-8'))
        key = m.hexdigest()

        m = md5()
        m.update((secret + key).encode('utf-8'))
        iv = m.hexdigest()

        aes = AES.new(key, AES.MODE_CBC, iv[:16])
        return str(un_pad(aes.decrypt(encoded)), 'utf-8')

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
