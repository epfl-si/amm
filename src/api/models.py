"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import binascii
import os


class APIKey:

    def __init__(self):
        self.access_key = self.generate_access_key()
        self.secret_key = self.generate_secret_key()

    def __str__(self):
        return self.access_key + self.secret_key

    @staticmethod
    def generate_access_key():
        return binascii.hexlify(os.urandom(20)).decode("utf-8")

    @staticmethod
    def generate_secret_key():
        return binascii.hexlify(os.urandom(40)).decode("utf-8")

    def get_id(self, username):
        return "key:%s:%s" % (username, self.access_key)
