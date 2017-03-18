"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import re
import ldap3

from config.settings import base


class Authenticator(object):
    """ Class to authenticate users using LDAP(S) """

    def __init__(self):
        self.ldap_server = base.get_config('LDAP_SERVER')
        self.protocol = 'ldaps' if base.get_config('LDAP_USE_SSL') == 'true' else 'ldap'

        self.use_ssl = True if base.get_config('LDAP_USE_SSL') == 'true' else False
        self.uri = self.protocol + '://' + self.ldap_server
        self.dn = base.get_config('LDAP_USER_BASE_DN')
        self.user_attr = base.get_config('LDAP_USER_SEARCH_ATTR')

    def get_user_dn(self, username):

        server = ldap3.Server('ldap://' + self.ldap_server)
        connection = ldap3.Connection(server)
        connection.open()

        connection.search(
            search_base=self.dn,
            search_filter='(' + self.user_attr + '=' + username + ')'
        )
        return connection.response[0]['dn']

    def authenticate(self, username, password):
        """ Authenticate the user with a bind on the LDAP server """

        if username is None or password is None:
            return False

        # check the username
        if not re.match("^[A-Za-z0-9_-]*$", username):
            return False

        user_dn = self.get_user_dn(username)

        server = ldap3.Server(
                self.uri,
                use_ssl=self.use_ssl
            )

        connection = ldap3.Connection(server, user=user_dn, password=password)

        return connection.bind()
