"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import binascii
import os
import hashlib


class APIKey:

    def __init__(self):
        self.access_key = self.generate_access_key()
        self.generate_secret_key()

    def __str__(self):
        return self.access_key + self.secret_key

    @staticmethod
    def generate_access_key():
        return binascii.hexlify(os.urandom(10)).decode("utf-8")

    def generate_secret_key(self):

        secret_key_clear_byte = binascii.hexlify(os.urandom(20))
        self.secret_key_clear = secret_key_clear_byte.decode("utf-8")
        self.secret_key = hashlib.sha256(secret_key_clear_byte).hexdigest()

    def get_id(self, username):
        return "key:%s:%s" % (username, self.access_key)

    def get_values(self):
        return {"access_key": self.access_key,
                "secret_key": self.secret_key_clear}
