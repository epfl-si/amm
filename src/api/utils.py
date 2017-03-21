"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import os
import string
import binascii

import ldap3


def generate_random_b64(length):
    """
    Generate a random string encoded with base 64
    """

    return binascii.hexlify(os.urandom(int(length / 2))).decode("utf-8")


def generate_password(length):
    """
    Generate a random password
    """

    chars = string.ascii_letters + string.digits + '-+'
    password = ''

    for i in range(length):

        password += chars[int(os.urandom(1)[0]) % len(chars)]

    return password


def get_connection_string(db_username, db_password, db_stack, db_env, db_port, db_schema):
    """
    Returns a connection string according to the given variables.
    """

    # mysql://username:password@mysql.db_stack.env.epfl.ch:1234/db_schema
    connection = "mysql://%s:%s@mysql.%s.%s.epfl.ch:%s/%s" % (db_username, db_password, db_stack,
                                                              db_env, db_port, db_schema)

    return connection


def get_connection_string_with_ip(db_username, db_password, db_ip, db_port, db_schema):
    """
    Returns a connection string according to the given variables.
    """

    # mysql://username:password@mysql.db_stack.env.epfl.ch:1234/db_schema

    if db_password:
        connection = "mysql://%s:%s@%s:%s/%s" % (db_username, db_password, db_ip, db_port, db_schema)
    else:
        connection = "mysql://%s@%s:%s/%s" % (db_username, db_ip, db_port, db_schema)

    return connection


def get_mysql_client_cmd(db_username, db_password, db_ip, db_port, db_schema):
    """
    Returns a connection string according to the given variables
    """

    if db_password:
        cmd = "mysql -h %s -u%s -p%s -P %s %s" % (db_ip, db_username, db_password, db_port, db_schema)
    else:
        cmd = "mysql -h %s -u%s -p -P %s %s" % (db_ip, db_username, db_port, db_schema)

    return cmd


def get_sciper(username, ldap_server='scoldap.epfl.ch', ldap_base='o=epfl,c=ch'):
    """ Return the sciper of user """

    server = ldap3.Server('ldap://' + ldap_server)
    connection = ldap3.Connection(server)
    connection.open()

    connection.search(
        search_base=ldap_base,
        search_filter='(uid=' + username + ')',
        attributes=['uniqueIdentifier']
    )
    return connection.response[0]['attributes']['uniqueIdentifier'][0]
