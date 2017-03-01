"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import requests
import json
import api.utils
from requests.auth import HTTPBasicAuth
from config.settings.base import get_config

STACKS = []


class Rancher(object):
    def __init__(self):
        pass

    def get(self, url, prefix=True):

        """Do an authenticated GET at the given URL and return the response"""

        if prefix:
            url = get_config("RANCHER_API_URL") + url

        return requests.get(url,
                            verify=get_config("RANCHER_VERIFY_CERTIFICATE").lower() == "true",
                            auth=HTTPBasicAuth(
                                get_config("RANCHER_ACCESS_KEY"),
                                get_config("RANCHER_SECRET_KEY")))

    def post(self, url, data, prefix=True):

        """Do an authenticated POST at the given URL and return the response"""

        if prefix:
            url = get_config("RANCHER_API_URL") + url

        return requests.post(url,
                             data=data,
                             verify=get_config("RANCHER_VERIFY_CERTIFICATE").lower() == "true",
                             auth=HTTPBasicAuth(
                                 get_config("RANCHER_ACCESS_KEY"),
                                 get_config("RANCHER_SECRET_KEY")))

    def get_template(self, template):

        """Returns a dict containing the given template data"""

        # first we retrieve the available versions for this template
        data = self.get("/v1-catalog/templates/" + template).json()

        # we want the default version
        version = data['defaultVersion']

        url = data['versionLinks'][version]

        return self.get(url, prefix=False).json()

    def create_mysql_stack(self):

        """Create a MySQL stack with default options"""

        template = self.get_template("idevelop:mysql")

        environment = {
            "MYSQL_VERSION": "5.5",
            "MYSQL_ROOT_PASSWORD": "",
            "MYSQL_DATABASE": api.utils.generate_random_b64(8),
            "AMM_USERNAME": api.utils.generate_random_b64(8),
            "AMM_USER_PASSWORD_HASH": api.utils.generate_password(20),  # TODO hash with sha1
            "MAX_CONNECTIONS": "151",
            "QUOTA_SIZE_MIB": "500",
            "MYSQL_EXPORT_PORT": "3306"
        }

        payload = {
            "system": False,
            "type": "stack",
            "name": "mysql-" + api.utils.generate_random_b64(8),
            "startOnCreate": True,
            "environment": environment,
            "description": "",
            "dockerCompose": template["files"]["docker-compose.yml"],
            "rancherCompose": template["files"]["rancher-compose.yml"],
            "externalId": "catalog://" + template["id"]}

        return self.post("/v2-beta/stacks", data=json.dumps(payload))

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
