

import base64


class Base64(object):

    @staticmethod
    def decrypt(value, key):
        return unicode(base64.b64decode(value))

    @staticmethod
    def encrypt(value, key):
        return base64.b64encode(value)
