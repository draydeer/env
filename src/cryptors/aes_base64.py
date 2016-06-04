

import base64

from Crypto.Cipher import AES


class AesBase64(object):

    @staticmethod
    def decrypt(value, key):
        return unicode(AES.new(key.rjust(16), AES.MODE_ECB).decrypt(base64.b64decode(value)).strip())

    @staticmethod
    def encrypt(value, key):
        return base64.b64encode(AES.new(key.rjust(16), AES.MODE_ECB).encrypt(value.rjust(16)))
