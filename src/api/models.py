"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import binascii
import os


class Key:

    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()

    def __str__(self):
        return self.public_key + self.private_key

    @staticmethod
    def generate_private_key():
        return binascii.hexlify(os.urandom(40))

    @staticmethod
    def generate_public_key():
        return binascii.hexlify(os.urandom(20))

    def get_apikey(self):
        return self.public_key + self.private_key