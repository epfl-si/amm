"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import binascii
import hashlib
from api import utils


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

    def generate_salt(self):
        """Generate the salt"""
        return utils.generate_password(20)

    def generate_access_key(self):
        """Generate the access key (public part)"""
        return utils.generate_random_b64(20)

    def generate_secret_key(self):
        """Generate the secret key (private part)"""
        self.secret_key_clear = utils.generate_password(40)

    def get_id(self, username):
        """Returns the APIKey's id"""
        return "key:%s:%s" % (username, self.access_key)

    def get_values(self):
        """Returns the APIkey values as a dict"""
        return {"access_key": self.access_key,
                "secret_key": self.secret_key_clear}

    def get_secret_key_hash(self):
        """Returns the secret key hashed"""
        if self.secret_key_hash is None:
            byteshash = hashlib.pbkdf2_hmac('sha256',
                                            self.secret_key_clear.encode('utf-8'),
                                            self.salt.encode('utf-8'),
                                            1)
            self.secret_key_hash = binascii.hexlify(byteshash).decode('utf-8')
        return self.secret_key_hash
