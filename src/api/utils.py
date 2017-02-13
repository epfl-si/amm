import re
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
