"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import binascii
import os
import hashlib


class APIKey:

    def __init__(self):
        self.access_key = None
        self.salt = None
        self.secret_key_hash = None
        self.secret_key_clear = None

    @staticmethod
    def generate():
        new = APIKey()
        new.salt = new.generate_salt()
        new.access_key = new.generate_access_key()
        new.generate_secret_key()
        return new

    def __str__(self):
        return self.access_key + self.get_secret_key_hash()

    @staticmethod
    def generate_salt():
        return binascii.hexlify(os.urandom(10)).decode("utf-8")

    def generate_access_key(self):
        return binascii.hexlify(os.urandom(10)).decode("utf-8")

    def generate_secret_key(self):

        secret_key_clear_byte = binascii.hexlify(os.urandom(20))
        self.secret_key_clear = secret_key_clear_byte.decode("utf-8")

    def get_id(self, username):
        return "key:%s:%s" % (username, self.access_key)

    def get_values(self):
        return {"access_key": self.access_key,
                "secret_key": self.secret_key_clear}

    def get_secret_key_hash(self):
        if self.secret_key_hash == None:
            byteshash = hashlib.pbkdf2_hmac('sha256', self.secret_key_clear.encode('utf-8'), self.salt.encode('utf-8'), 1)
            self.secret_key_hash = binascii.hexlify(byteshash).decode('utf-8')
        return self.secret_key_hash
