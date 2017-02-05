from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS


def get_ldap_connection():
    return Connection(Server('ldap.epfl.ch', port=636, use_ssl=True),
                      auto_bind=AUTO_BIND_NO_TLS,
                      read_only=True,
                      check_names=True,
                      user='charmier',
                      password='toto')

