"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import re
import ldap3

from config.settings import base


class Authenticator(object):
    """ Class to authenticate users using LDAP(S) """

    def __init__(self):
        server = base.get_config('LDAP_SERVER')
        scheme = 'ldaps' if base.get_config('LDAP_USE_SSL') == 'true' else 'ldap'

        self.use_ssl = True if base.get_config('LDAP_USE_SSL') == 'true' else False,
        self.uri = scheme + '://' + server
        self.userdn = base.get_config('LDAP_USER_BASE_DN')
        self.user_attr = base.get_config('LDAP_USER_SEARCH_ATTR')

    def authenticate(self, username, password):
        """ authenticate the user with a secure bind on the LDAP server """

        if username is None or password is None:
            return False

        # check the username
        if not re.match("^[A-Za-z0-9_-]*$", username):
            return False

        dn = self.user_attr + "=" + username + "," + self.userdn

        s = ldap3.Server(
                self.uri,
                use_ssl=self.use_ssl
            )

        c = ldap3.Connection(s, user=dn, password=password)

        return c.bind()
