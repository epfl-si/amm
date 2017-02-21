"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import os
import string
import binascii


def generate_random_b64(length):
    """ Generate a random string encoded with base 64 """

    return binascii.hexlify(os.urandom(int(length / 2))).decode("utf-8")


def generate_password(length):
    """ Generate a random password """

    chars = string.ascii_letters + string.digits + '-+'

    password = ''

    for i in range(length):

        password += chars[int(os.urandom(1)[0]) % len(chars)]

    return password
