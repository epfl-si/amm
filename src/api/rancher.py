"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

CONNECTIONS = []


class Rancher(object):
    def __init__(self):
        pass

    def create_stack(self, requester, db_username, db_password, db_port, db_schema, db_stack, db_env):
        """Create a db stack with the given informations"""
        connection = {

            'requester': requester,
            'db_username': db_username,
            'db_password': db_password,
            'db_port': db_port,
            'db_schema': db_schema,
            'db_stack': db_stack,
            'db_env': db_env
        }

        CONNECTIONS.append(connection)
        return connection

    def get_stacks(self, requester):
        """Returns the stacks of the given users"""

        result = []

        for connection in CONNECTIONS:

            if requester == connection['requester']:

                result.append(connection)

        return result
