"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import hashlib
import json
import requests

from random import randint
from time import sleep

from django.conf import settings
from requests.auth import HTTPBasicAuth

from config.settings.base import get_config
from .utils import generate_password, generate_random_b64, get_mysql_client_cmd, get_connection_string


class Rancher:

    @staticmethod
    def init_http_call(url, prefix=True):
        """
        Init http call
        """
        if prefix:
            url = get_config("RANCHER_API_URL") + url

        parameters = {
            'verify': get_config("RANCHER_VERIFY_CERTIFICATE").lower() == "true",
            'auth': HTTPBasicAuth(
                get_config("RANCHER_ACCESS_KEY"),
                get_config("RANCHER_SECRET_KEY")
            )
        }

        return url, parameters

    @classmethod
    def get(cls, url, prefix=True):
        """
        Do an authenticated GET at the given URL and return the response
        """
        url, parameters = cls.init_http_call(url, prefix)

        return requests.get(url, **parameters)

    @classmethod
    def post(cls, url, data, prefix=True):
        """
        Do an authenticated POST at the given URL and return the response
        """
        url, parameters = cls.init_http_call(url, prefix)

        return requests.post(url, data=data, **parameters)

    @classmethod
    def put(cls, url, data, prefix=True):
        """
        Do an authenticated PUT at the given URL and return the response
        """
        url, parameters = cls.init_http_call(url, prefix)

        return requests.put(url, data=data, **parameters)

    @classmethod
    def delete(cls, url, prefix=True):
        """
        Do an authenticated DELETE at the given URL and return the response
        """
        url, parameters = cls.init_http_call(url, prefix)

        return requests.delete(url, **parameters)

    @classmethod
    def get_template(cls, template):
        """
        Returns a dict containing the given template data
        """
        # first we retrieve the available versions for this template
        data = cls.get("/v1-catalog/templates/" + template).json()

        # we want the default version
        version = data['defaultVersion']

        url = data['versionLinks'][version]

        return cls.get(url, prefix=False).json()

    @classmethod
    def get_ports_used(cls):
        """
        Return the list of ports used
        """
        ports = cls.get("/v2-beta/projects/" + settings.ENVIRONMENT_ID + "/ports").json()["data"]
        return [str(current_port["publicPort"]) for current_port in ports]

    @classmethod
    def get_available_port(cls):
        """
        Generate an available port
        """
        ports_used = cls.get_ports_used()
        while True:
            new_port = randint(1, 65536)
            if new_port not in ports_used:
                return new_port

    @classmethod
    def _get_environment(cls, password):
        """
        Return environment information
        """
        password_hash = '*' + hashlib.sha1(hashlib.sha1(password.encode('utf-8')).digest()).hexdigest()

        return {
            "MYSQL_VERSION": "5.5",
            "MYSQL_ROOT_PASSWORD": generate_password(20),
            "MYSQL_DATABASE": generate_random_b64(8),
            "AMM_USERNAME": generate_random_b64(8),
            "AMM_USER_PASSWORD_HASH": password_hash,
            "MAX_CONNECTIONS": "151",
            "QUOTA_SIZE_MIB": "500",
            "MYSQL_EXPORT_PORT": cls.get_available_port()
        }

    @classmethod
    def _get_payload(cls, environment, sciper, unit_id):
        """
        Return payload of stack
        """

        template = cls.get_template("idevelop:mysql")

        payload = {
            "system": False,
            "type": "stack",
            "name": "mysql-" + generate_random_b64(8),
            "startOnCreate": True,
            "environment": environment,
            "description": "",
            "dockerCompose": template["files"]["docker-compose.yml"],
            "rancherCompose": template["files"]["rancher-compose.yml"],
            "externalId": "catalog://" + template["id"],
            "group": "owner:" + sciper + "," + "unit:" + unit_id
        }

        return payload

    @classmethod
    def _create_mysql_stack(cls, sciper, password, unit_id):
        """
        Create a MySQL stack with default options
        """
        environment = cls._get_environment(password=password)
        payload = cls._get_payload(environment=environment, sciper=sciper, unit_id=unit_id)
        mysql_stack = cls.post("/v2-beta/stacks", data=json.dumps(payload))

        # wait a bit for the stack to be created
        sleep(5)

        return mysql_stack, payload, environment

    @classmethod
    def update_stack(cls, stack, unit_id):

        url = "/v2-beta/projects/" + settings.ENVIRONMENT_ID + "/stacks/" + stack["id"]
        new_group = stack["group"].split(',unit:')[0] + ',unit:' + unit_id
        data = {"group": new_group}
        cls.put(url, data=data)

    @classmethod
    def create_mysql_stack(cls, sciper, unit_id):

        password = generate_password(20)

        mysql_stack, payload, environment = cls._create_mysql_stack(sciper, password, unit_id)

        data = {
            "response": mysql_stack,
            "db_password": password,
            "db_username": environment["AMM_USERNAME"],
            "db_schema": environment["MYSQL_DATABASE"],
            "db_host": payload["name"] + settings.DOMAIN,
            "db_port": environment["MYSQL_EXPORT_PORT"],
            "stack": payload["name"],
            "unit_id": unit_id
        }

        parameters = [
            data["db_username"],
            data["db_password"],
            data["db_host"],
            data["db_port"],
            data["db_schema"]
        ]

        data["connection_string"] = get_connection_string(*parameters)
        data["mysql_cmd"] = get_mysql_client_cmd(*parameters)
        data["schema_id"] = payload["name"].split('-')[1]

        return data

    @classmethod
    def validate(cls, schema_id, sciper):
        """
        Check if the schema 'schema_id' belongs to user (id = sciper)
        """
        stack_name = "mysql-" + schema_id
        user_stacks = cls.get_stacks_by_user(sciper)

        return stack_name in [stack['name'] for stack in user_stacks]

    @classmethod
    def get_stacks_by_user(cls, user_id):
        """
        Returns the stacks of the given users
        """
        url = "/v2-beta/projects/" + settings.ENVIRONMENT_ID + "/stacks/?group_like=owner%3A" + user_id + "%25"
        return cls.get(url).json()["data"]

    @classmethod
    def get_stacks_by_unit(cls, unit_id):
        """
        Returns the stacks filter by unit 'unit_id'
        """
        url = "/v2-beta/projects/" + settings.ENVIRONMENT_ID + "/stacks/?group_like=%25unit%3A" + unit_id
        return cls.get(url).json()["data"]

    @classmethod
    def get_stacks_by_unit_and_user(cls, unit_id, user_id):
        """
        Returns the stacks filter by unit 'unit_id' and user 'user_id'
        """
        url = "/v2-beta/projects/" + settings.ENVIRONMENT_ID
        url += "/stacks/?group_like=owner%3A" + user_id + "%2Cunit%3A" + unit_id
        return cls.get(url).json()["data"]

    @classmethod
    def get_stack(cls, name_stack):
        """
        Return the stack whith the name 'name_stack'
        Example :
        /v2-beta/projects/1a9/stacks/?name=mysql-e9608f8f
        """
        return cls.get("/v2-beta/projects/" + settings.ENVIRONMENT_ID + "/stacks/?name=" + name_stack).json()["data"]

    @classmethod
    def get_mysql_user(cls, schema_id):
        name_stack = "mysql-" + schema_id
        stack = cls.get_stack(name_stack=name_stack)[0]
        return stack['environment']['AMM_USERNAME']

    @classmethod
    def get_schema(cls, schema_id):
        """
        Returns the schema of the given user
        """
        name_stack = "mysql-" + schema_id
        stack = cls.get_stack(name_stack=name_stack)[0]

        parameters = [
            stack['environment']['AMM_USERNAME'],
            None,
            name_stack + settings.DOMAIN,
            stack['environment']['MYSQL_EXPORT_PORT'],
            stack['environment']['MYSQL_DATABASE']
        ]

        schema = {
            "connection_string": get_connection_string(*parameters),
            "mysql_cmd": get_mysql_client_cmd(*parameters),

            # Example of stack['group'] = 'owner:133134,unit:1303'
            "unit_id": stack['group'].split(',unit:')[1],
            "schema_id": schema_id
        }
        return schema

    @classmethod
    def update_schema(cls, schema_id, unit_id):
        """
        Update schema to modify unit_id
        """
        stack = cls.get_stack(name_stack="mysql-" + schema_id)[0]
        cls.update_stack(stack, unit_id)

    @classmethod
    def __get_schemas(cls, stacks):

        schemas = []

        for stack in stacks:
            parameters = [
                stack['environment']['AMM_USERNAME'],
                None,
                stack["name"] + settings.DOMAIN,
                stack['environment']['MYSQL_EXPORT_PORT'],
                stack['environment']['MYSQL_DATABASE']
            ]

            schemas.append(
                {
                    "connection_string": get_connection_string(*parameters),
                    "mysql_cmd": get_mysql_client_cmd(*parameters),
                    # Example of stack['group'] = 'owner:133134,unit:13030'
                    "unit_id": stack['group'].split(',unit:')[1],
                    "schema_id": stack["name"].split("-")[1]
                }
            )

        return schemas

    @classmethod
    def get_schemas_by_user(cls, sciper):
        """
        Returns the schemas of the given user
        """
        schemas = cls.__get_schemas(stacks=cls.get_stacks_by_user(sciper))
        return schemas

    @classmethod
    def get_schemas_by_unit(cls, unit_id):
        """
        Returns all schemas filter by unit 'unit_id'
        """
        schemas = cls.__get_schemas(stacks=cls.get_stacks_by_unit(unit_id))
        return schemas

    @classmethod
    def get_schemas_by_unit_and_user(cls, unit_id, user_id):
        """
        Returns all schemas filter by unit 'unit_id' and user 'user_id'
        """
        schemas = cls.__get_schemas(stacks=cls.get_stacks_by_unit_and_user(unit_id, user_id))
        return schemas

    @classmethod
    def delete_schema(cls, schema_id):
        """
        Delete schema 'schema_id'
        """
        stack_id = cls.get_stack(name_stack="mysql-" + schema_id)[0]['id']
        cls.delete_stack(stack_id)

    @classmethod
    def delete_stack(cls, stack_id):
        """
        Delete the stack 'stack_id'
        """
        cls.delete("/v2-beta/projects/" + settings.ENVIRONMENT_ID + "/stacks/" + stack_id)

    @classmethod
    def clean_stacks(cls, sciper):
        """
        Delete all stacks created by user 'sciper'
        """

        # Return stacks by sciper
        stacks = cls.get_stacks_by_user(sciper)

        sleep(10)

        # Delete all stacks
        for stack in stacks:
            stack_id = stack["id"]
            cls.delete_stack(stack_id)
