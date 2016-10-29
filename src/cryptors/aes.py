
from Crypto.Cipher import AES


class Aes(object):

    @staticmethod
    def decrypt(value, key):
        return AES.new(key.rjust(16), AES.MODE_ECB).decrypt(value).strip()

    @staticmethod
    def encrypt(value, key):
        return AES.new(key.rjust(16), AES.MODE_ECB).encrypt(value.rjust(16))
