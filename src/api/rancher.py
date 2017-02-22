"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

STACKS = []


class Rancher(object):
    def __init__(self):
        pass

    def create_stack(self, requester, db_username, db_password, db_port, db_schema, db_stack, db_env):

        """Create a db stack with the given informations"""
        stack = {

            'requester': requester,
            'db_username': db_username,
            'db_port': db_port,
            'db_schema': db_schema,
            'db_stack': db_stack,
            'db_env': db_env
        }

        STACKS.append(stack)

        return stack

    def get_stacks(self, requester):
        """Returns the stacks of the given users"""

        stacks = []

        for stack in STACKS:

            if requester == stack['requester']:
                stacks.append(stack)

        return stacks

    def get_schemas(self, requester):
        """Returns the schemas of the given users"""

        schemas = []

        stacks = self.get_stacks(requester)

        for stack in stacks:

            db_username = stack['db_username']
            db_stack = stack['db_stack']
            db_env = stack['db_env']
            db_port = stack['db_port']
            db_schema = stack['db_schema']

            schema = "mysql://%s:?????@mysql.%s.%s.epfl.ch:%s/%s" % (db_username, db_stack,
                                                                     db_env, db_port, db_schema)
            schemas.append(schema)

        return schemas
