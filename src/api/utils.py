import re
from ldap3 import Server, Connection

from config.settings.base import LDAP_SERVER, LDAP_BASE


def authenticate(username, password):
    """ authenticate the user with a secure bind on the LDAP server """

    # check the username
    if not re.match("^[A-Za-z0-9_-]*$", username):
        return False

    dn = "uid=" + username + "," + LDAP_BASE

    s = Server(LDAP_SERVER, use_ssl=True)

    c = Connection(s, user=dn, password=password)

    return c.bind()
