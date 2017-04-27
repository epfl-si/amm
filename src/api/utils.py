"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import os
import string
import binascii
import ldap3
from django.conf import settings

from config.settings import base


def generate_random_b64(length):
    """
    Generate a random string encoded with base 64
    """
    return binascii.hexlify(os.urandom(int(length / 2))).decode("utf-8")


def generate_password(length):
    """
    Generate a random password
    """
    # the chars we are going to use. We don't use the plus sign (+) because
    # it's problematic in URLs
    chars = string.ascii_letters + string.digits + '-.'
    password = ''

    for i in range(length):
        password += chars[int(os.urandom(1)[0]) % len(chars)]

    return password


def get_connection_string(db_username, db_password, db_host, db_port, db_schema):
    """
    Returns a connection string according to the given variables.
    Format:
    mysql://username:password@mysql.db_stack.env.epfl.ch:1234/db_schema
    Example:
    mysql://aa2ea71b:-CxMbtSVdPcY88MH3Vo7@mysql-78bc59f0.db.rsaas.epfl.ch:12068/98c321cb
    """

    if db_password:
        connection = "mysql://%s:%s@%s:%s/%s" % (db_username, db_password, db_host, db_port, db_schema)
    else:
        connection = "mysql://%s@%s:%s/%s" % (db_username, db_host, db_port, db_schema)
    return connection


def get_mysql_client_cmd(db_username, db_password, db_host, db_port, db_schema):
    """
    Returns a connection string according to the given variables
    """
    if db_password:
        cmd = "mysql -h %s -u%s -p%s -P %s %s" % (db_host, db_username, db_password, db_port, db_schema)
    else:
        cmd = "mysql -h %s -u%s -p -P %s %s" % (db_host, db_username, db_port, db_schema)
    return cmd


def _get_LDAP_connection():
    """
    Return a LDAP connection
    """
    ldap_server = base.get_config('LDAP_SERVER_FOR_SEARCH')
    ldap_base = base.get_config('LDAP_BASE_DN')

    server = ldap3.Server('ldap://' + ldap_server)
    connection = ldap3.Connection(server)
    connection.open()

    return connection, ldap_base


def LDAP_search(pattern_search, attribute):
    """
    Do a LDAP search
    """
    connection, ldap_base = _get_LDAP_connection()

    connection.search(
        search_base=ldap_base,
        search_filter=pattern_search,
        attributes=[attribute]
    )
    return connection.response


def is_unit_exist(unit_id):
    """
    Return True if the unit 'unid_id' exists.
    Otherwise return False
    """
    attribute = 'objectClass'
    response = LDAP_search(
        pattern_search="(uniqueidentifier=" + unit_id + ")",
        attribute=attribute
    )

    try:
        return 'EPFLorganizationalUnit' in response[0]['attributes'][attribute]
    except Exception as error:
        return False


def get_unit_name(unit_id):
    """
    Return the unit name to the unit 'unit_id'
    """
    attribute = 'cn'
    response = LDAP_search(
        pattern_search='(uniqueIdentifier=' + unit_id + ')',
        attribute=attribute
    )
    return response[0]['attributes'][attribute][0]


def get_units(username):
    """
    Return all units of user 'username'
    """
    connection, ldap_base = _get_LDAP_connection()

    # Search the user dn
    connection.search(
        search_base=ldap_base,
        search_filter='(uid=' + username + '@*)',
    )

    # For each user dn give me the unit
    dn_list = [connection.response[index]['dn'] for index in range(len(connection.response))]

    units = []
    # For each unit search unit information and give me the unit id
    for dn in dn_list:
        unit = dn.split(",ou=")[1]
        connection.search(search_base=ldap_base, search_filter='(ou=' + unit + ')', attributes=['uniqueidentifier'])
        units.append(connection.response[0]['attributes']['uniqueIdentifier'][0])

    return units


def get_sciper(username):
    """
    Return the sciper of user
    """
    attribute = 'uniqueIdentifier'
    response = LDAP_search(
        pattern_search='(uid=' + username + ')',
        attribute=attribute
    )
    return response[0]['attributes'][attribute][0]


def get_username(sciper):
    """
    return username of user
    """
    attribute = 'uid'
    response = LDAP_search(
        pattern_search='(uniqueIdentifier=' + sciper + ')',
        attribute=attribute
    )
    return response[0]['attributes'][attribute][0]


def https_url(url):
    """
    Make sure the url is in https
    """
    return url.replace("http://", "https://")


def old_debug(string_to_display):
    import sys
    sys.stderr.write("**************************************************")
    sys.stderr.write("**************************************************")
    sys.stderr.write("**************************************************")
    sys.stderr.write(str(string_to_display))
    sys.stderr.write("**************************************************")
    sys.stderr.write("**************************************************")
    sys.stderr.write("**************************************************")
