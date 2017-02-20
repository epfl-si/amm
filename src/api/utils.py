import re
import os
import string
import binascii
from ldap3 import Server, Connection

from config.settings.base import get_config


def authenticate(username, password):
    """ authenticate the user with a secure bind on the LDAP server """

    # check the username
    if not re.match("^[A-Za-z0-9_-]*$", username):
        return False

    dn = get_config('LDAP_USER_SEARCH_ATTR') + "=" + username + "," + get_config('LDAP_USER_BASE_DN')

    s = Server(get_config('LDAP_SERVER'), use_ssl=True)

    c = Connection(s, user=dn, password=password)

    return c.bind()


def generate_random_b64(length):

    return binascii.hexlify(os.urandom(int(length / 2))).decode("utf-8")


def generate_password(length):

    chars = string.ascii_letters + string.digits + '-+'

    password = ''

    for i in range(length):

        password += chars[int(os.urandom(1)[0]) % len(chars)]

    return password
