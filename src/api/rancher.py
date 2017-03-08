"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import hashlib
import json
from random import randint
from time import sleep

import requests
from requests.auth import HTTPBasicAuth

import api.utils
from api import utils
from config.settings.base import get_config


# TODO get this dynamically
ENVIRONMENT_ID = "1a7"


class Rancher(object):
    def __init__(self):
        pass

    def get(self, url, prefix=True):
        """
        Do an authenticated GET at the given URL and return the response
        """

        if prefix:
            url = get_config("RANCHER_API_URL") + url

        return requests.get(url,
                            verify=get_config("RANCHER_VERIFY_CERTIFICATE").lower() == "true",
                            auth=HTTPBasicAuth(
                                get_config("RANCHER_ACCESS_KEY"),
                                get_config("RANCHER_SECRET_KEY")))

    def post(self, url, data, prefix=True):
        """
        Do an authenticated POST at the given URL and return the response
        """

        if prefix:
            url = get_config("RANCHER_API_URL") + url

        return requests.post(url,
                             data=data,
                             verify=get_config("RANCHER_VERIFY_CERTIFICATE").lower() == "true",
                             auth=HTTPBasicAuth(
                                 get_config("RANCHER_ACCESS_KEY"),
                                 get_config("RANCHER_SECRET_KEY")))

    def delete(self, url, prefix=True):

        if prefix:
            url = get_config("RANCHER_API_URL") + url

        return requests.delete(url,
                               verify=get_config("RANCHER_VERIFY_CERTIFICATE").lower() == "true",
                               auth=HTTPBasicAuth(
                                 get_config("RANCHER_ACCESS_KEY"),
                                 get_config("RANCHER_SECRET_KEY")))

    def get_template(self, template):
        """
        Returns a dict containing the given template data
        """

        # first we retrieve the available versions for this template
        data = self.get("/v1-catalog/templates/" + template).json()

        # we want the default version
        version = data['defaultVersion']

        url = data['versionLinks'][version]

        return self.get(url, prefix=False).json()

    def get_ports_used(self):
        """
        Return the list of ports used
        """
        ports = []
        response = self.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/ports")
        ports = response.json()["data"]
        for current_port in ports:
            if "publicPort" in current_port:
                ports.append(str(current_port["publicPort"]))
        return ports

    def get_available_port(self):
        """
        Generate an available port
        """
        while True:
            new_port = randint(1, 65536)
            if new_port not in self.get_ports_used():
                return new_port

    def create_mysql_stack(self, sciper):
        """
        Create a MySQL stack with default options
        """

        data = {}

        template = self.get_template("idevelop:mysql")

        password = api.utils.generate_password(20)

        password_hash = '*' + hashlib.sha1(hashlib.sha1(password.encode('utf-8')).digest()).hexdigest()

        environment = {
            "MYSQL_VERSION": "5.5",
            "MYSQL_ROOT_PASSWORD": api.utils.generate_password(20),
            "MYSQL_DATABASE": api.utils.generate_random_b64(8),
            "AMM_USERNAME": api.utils.generate_random_b64(8),
            "AMM_USER_PASSWORD_HASH": password_hash,
            "MAX_CONNECTIONS": "151",
            "QUOTA_SIZE_MIB": "500",
            "MYSQL_EXPORT_PORT": self.get_available_port()
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
            "externalId": "catalog://" + template["id"],
            "group": "owner:" + sciper
        }

        response = self.post("/v2-beta/stacks", data=json.dumps(payload))

        data["response"] = response
        data["db_password"] = password
        data["db_username"] = environment["AMM_USERNAME"]
        data["db_schema"] = environment["MYSQL_DATABASE"]
        data["db_port"] = environment["MYSQL_EXPORT_PORT"]
        data["stack"] = payload["name"]

        # wait a bit for the stack to be created
        sleep(5)

        stack_data = data["response"].json()

        stack_id = stack_data["id"]

        ip = self.get_ip_address(stack_id)

        connection_string = utils.get_connection_string_with_ip(
            data["db_username"],
            data["db_password"],
            ip,
            data["db_port"],
            data["db_schema"]
        )

        mysql_cmd = utils.get_mysql_client_cmd(
            data["db_username"],
            data["db_password"],
            ip,
            data["db_port"],
            data["db_schema"]
        )

        data["connection_string"] = connection_string
        data["mysql_cmd"] = mysql_cmd

        return data

    def get_ip_address(self, stack_id):
        """
        Return ip address
        """
        services_response = self.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/stacks/" + stack_id + "/services")

        if len(services_response.json()["data"]) != 1:
            # This stack returns many services
            # How to know which service should be used
            pass
        else:
            service_id = services_response.json()["data"][0]["id"]

        service_response = self.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/services/" + service_id)

        ip_address = service_response.json()["publicEndpoints"][0]["ipAddress"]

        return ip_address

    def get_stacks(self, sciper):
        """
        Returns the stacks of the given users
        """
        user_stacks = []
        response = self.get("/v2-beta/projects/" + ENVIRONMENT_ID + "/stacks/")
        stacks = response.json()["data"]

        for stack in stacks:
            tag = stack["group"]
            if tag and 'owner:' + sciper in tag:
                user_stacks.append(stack)

        return user_stacks

    def get_schemas(self, sciper):
        """
        Returns the schemas of the given users
        """
        schemas = []

        stacks = self.get_stacks(sciper)

        for stack in stacks:
            schema = utils.get_connection_string_with_ip(
                db_username=stack['environment']['AMM_USERNAME'],
                db_password=stack['environment']['AMM_USER_PASSWORD_HASH'],
                ip=self.get_ip_address(stack["id"]),
                db_port=stack['environment']['MYSQL_EXPORT_PORT'],
                db_schema=stack['environment']['MYSQL_DATABASE'])
            schemas.append(schema)

        return schemas

    def delete_stack(self, stack_id):
        """
        Delete the stack 'stack_id'
        """
        self.delete("/v2-beta/projects/" + ENVIRONMENT_ID + "/stacks/" + stack_id)

    def clean_stacks(self, sciper):
        """
        Delete all stacks created by user 'sciper'
        """

        # Return stacks by sciper
        stacks = self.get_stacks(sciper)

        sleep(10)

        # Delete all stacks
        for stack in stacks:
            stack_id = stack["id"]
            self.delete_stack(stack_id)
