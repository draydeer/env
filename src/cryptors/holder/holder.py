

from ..aes import Aes
from ..aes_base64 import AesBase64
from ..base_64 import Base64
from src.errors import NotExistsError


class Holder(object):

    initiators = {
        'aes': Aes,
        'aesBase64': AesBase64,
        'base64': Base64,
    }

    @staticmethod
    def get(k):
        if k in Holder.initiators:
            return Holder.initiators[k]

        raise NotExistsError("Cryptor not exists: %s" % k)
