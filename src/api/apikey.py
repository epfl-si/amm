"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import binascii
import hashlib
from api import utils


class APIKey:

    def __init__(self, access_key=None, secret_key=None, salt=None):

        self.secret_key_hash = None

        if access_key and secret_key and salt:
            self.access_key = access_key
            self.salt = salt
            self.secret_key_clear = secret_key
        else:
            self.__generate()

        self.__set_secret_key_hash()

    def __generate(self):
        self.__generate_salt()
        self.__generate_access_key()
        self.__generate_secret_key()

    def __generate_salt(self):
        """
        Generate the salt
        """
        self.salt = utils.generate_password(20)

    def __generate_access_key(self):
        """
        Generate the access key (public part)
        """
        self.access_key = utils.generate_random_b64(20)

    def __generate_secret_key(self):
        """
        Generate the secret key (private part)
        """
        self.secret_key_clear = utils.generate_password(40)

    def __set_secret_key_hash(self):
        """
        Returns the secret key hashed
        """
        if self.secret_key_hash is None:
            bytes_hash = hashlib.pbkdf2_hmac(
                'sha256',
                self.secret_key_clear.encode('utf-8'),
                self.salt.encode('utf-8'),
                1
            )
            self.secret_key_hash = binascii.hexlify(bytes_hash).decode('utf-8')

    def __str__(self):
        return self.access_key + self.secret_key_hash

    def get_id(self, username):
        """
        Returns the APIKey's id
        """
        return "key:%s:%s" % (username, self.access_key)

    def get_values(self):
        """
        Returns the APIkey values as a dict
        """
        return {"access_key": self.access_key,
                "secret_key": self.secret_key_clear}
