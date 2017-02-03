"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""


class Key:

    def __init__(self, username, private_key, public_key):
        self.username = username
        self.private_key = private_key
        self.public_key = public_key

    def __str__(self):
        return self.username + self.public_key + self.private_key
