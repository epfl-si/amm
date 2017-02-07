import ldap
import ldap.dn

# LDAP (secure connection)
LDAP_URL = "ldaps://scoldap.epfl.ch"
LDAP_SUCCESS_CODE = 97


def authenticate(username, password):

    ldap_conn = get_ldap()

    # escape the username because it's part of a dn
    username = ldap.dn.escape_dn_chars(username)

    dn = "uid=" + username + ",ou=users,o=epfl,c=ch"

    result = ldap_conn.simple_bind_s(dn, password)

    return result[0] == LDAP_SUCCESS_CODE


def get_ldap():
    """
    Returns an LDAP connection.

    :return an LDAP connection.
    """

    return ldap.initialize(LDAP_URL)