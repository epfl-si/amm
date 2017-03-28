"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import hashlib
import json
import requests

from random import randint
from time import sleep
from requests.auth import HTTPBasicAuth

from config.settings.base import get_config

from .utils import generate_password, generate_random_b64, get_connection_string_with_ip, get_mysql_client_cmd

# TODO get this dynamically
ENVIRONMENT_ID = "1a9"


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
        ports_used = []
        ports = cls.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/ports").json()["data"]
        for current_port in ports:
            if "publicPort" in current_port:
                ports_used.append(str(current_port["publicPort"]))
        return ports_used

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
    def _get_payload(cls, environment, sciper, unit):
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
            "group": "owner:" + sciper,
        }

        if unit:
            payload["group"] = "unit:" + unit

        return payload

    @classmethod
    def _create_mysql_stack(cls, sciper, password, unit):
        """
        Create a MySQL stack with default options
        """
        environment = cls._get_environment(password=password)
        payload = cls._get_payload(environment=environment, sciper=sciper, unit=unit)
        mysql_stack = cls.post("/v2-beta/stacks", data=json.dumps(payload))

        # wait a bit for the stack to be created
        sleep(5)

        return mysql_stack, payload, environment

    @classmethod
    def create_mysql_stack(cls, sciper, unit):

        password = generate_password(20)

        mysql_stack, payload, environment = cls._create_mysql_stack(sciper, password, unit)

        data = {
            "response": mysql_stack,
            "db_password": password,
            "db_username": environment["AMM_USERNAME"],
            "db_schema": environment["MYSQL_DATABASE"],
            "db_port": environment["MYSQL_EXPORT_PORT"],
            "stack": payload["name"]
        }

        parameters = [
            data["db_username"],
            data["db_password"],
            cls.get_ip_address(data["response"].json()["id"]),
            data["db_port"],
            data["db_schema"]
        ]

        # todo When we will replace ip by host we could replace *parameters by *data
        data["connection_string"] = get_connection_string_with_ip(*parameters)
        data["mysql_cmd"] = get_mysql_client_cmd(*parameters)

        return data

    @classmethod
    def get_ip_address(cls, stack_id):
        """
        Return ip address
        """
        services_response = cls.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/stacks/" + stack_id + "/services")

        if len(services_response.json()["data"]) != 1:
            # This stack returns many services
            # How to know which service should be used
            pass
        else:
            service_id = services_response.json()["data"][0]["id"]

        service_response = cls.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/services/" + service_id)

        ip_address = service_response.json()["publicEndpoints"][0]["ipAddress"]

        return ip_address

    @classmethod
    def get_stacks(cls, sciper):
        """
        Returns the stacks of the given users
        """
        user_stacks = []

        # TODO use a real requests, don't go through all the stacks
        stacks = cls.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/stacks/").json()["data"]
        for stack in stacks:
            tag = stack["group"]
            if tag and 'owner:' + sciper in tag:
                user_stacks.append(stack)

        return user_stacks

    @classmethod
    def get_schemas(cls, sciper):
        """
        Returns the schemas of the given users
        """
        schemas = []

        for stack in cls.get_stacks(sciper):
            parameters = [
                stack['environment']['AMM_USERNAME'],
                None,
                cls.get_ip_address(stack["id"]),
                stack['environment']['MYSQL_EXPORT_PORT'],
                stack['environment']['MYSQL_DATABASE']
            ]

            schemas.append(
                {
                    "connection_string": get_connection_string_with_ip(*parameters),
                    "mysql_cmd": get_mysql_client_cmd(*parameters)
                }
            )

        return schemas

    @classmethod
    def delete_stack(cls, stack_id):
        """
        Delete the stack 'stack_id'
        """
        cls.delete("/v2-beta/projects/" + ENVIRONMENT_ID + "/stacks/" + stack_id)

    @classmethod
    def clean_stacks(cls, sciper):
        """
        Delete all stacks created by user 'sciper'
        """

        # Return stacks by sciper
        stacks = cls.get_stacks(sciper)

        sleep(10)

        # Delete all stacks
        for stack in stacks:
            stack_id = stack["id"]
            cls.delete_stack(stack_id)
