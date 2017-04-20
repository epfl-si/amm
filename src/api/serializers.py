"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import auth
import requests

from rest_framework import serializers
from rest_framework.exceptions import APIException

from api.accred import is_db_admin
from config.settings.base import get_config
from .apikeyhandler import ApiKeyHandler
from .rancher import Rancher
from .utils import get_sciper, get_units, is_unit_exist, get_unit_name, generate_password


class KeySerializer(serializers.Serializer):
    """
    API Key Serializer
    """
    username = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)

    def validate(self, attrs):
        """
        Validate the user authentication
        """
        username = attrs.get('username')
        password = attrs.get('password')

        result = {}

        if username and password:

            authenticator = auth.get_configured_authenticator()

            if authenticator.authenticate(username=username, password=password):
                result["username"] = username

        if not result:
            raise serializers.ValidationError("Authentication failed", code='authorization')

        return result

    def create(self, validated_data):
        """
        Create the APIKeys
        """
        return ApiKeyHandler.generate_keys(validated_data["username"])


class PasswordSerializer(serializers.Serializer):
    """
    Password serializer
    """
    access_key = serializers.CharField(max_length=256)
    secret_key = serializers.CharField(max_length=256)

    def validate(self, attrs):
        """
        Validate the APIKeys
        """
        result = {}

        # Get required parameters
        access_key = attrs.get('access_key')
        secret_key = attrs.get('secret_key')

        # Check API Keys exist and return username
        result["username"] = ApiKeyHandler.validate(access=access_key, secret=secret_key)

        return result

    def create(self, validated_data):
        """
        Create a new mysql password
        """
        schema_id = validated_data["schema_id"]

        REST_API_ADDRESS = get_config("REST_API_ADDRESS") % {'stack': "mysql-" + schema_id}

        data = {
            "password": generate_password(length=20)
        }

        url = "http://" + REST_API_ADDRESS + "/v1/users/" + Rancher.get_mysql_user(schema_id) + "/"

        response = requests.patch(url, data=data)

        if response == 200:
            schema = Rancher.get_schema(schema_id)
            return {
                "connection_string": schema["connection_string"],
                "mysql_cmd": schema["mysql_cmd"],
                "unit_id": schema["unit_id"],
                "schema_id": schema["schema_id"]
            }
        else:
            raise APIException("Database password has not changed", code='error')


class SchemaSerializer(serializers.Serializer):
    """
    Schema Serializer
    """
    access_key = serializers.CharField(max_length=256)
    secret_key = serializers.CharField(max_length=256)
    unit_id = serializers.CharField(max_length=256, required=False)

    @staticmethod
    def _manage_units(username, unit_id, result):
        """
        If an unit is given, check is the user 'username' belongs to the unit 'unit'.
        If no unit is given, find all units of user 'username' and :
        -> if the user have many units then ValidationError
        -> if the user have only one unit, we associate this one
        """

        # Return all the unit of user
        units = get_units(username)

        if not unit_id:
            if len(units) > 1:
                msg = "User has more one unit"
                for unit_id in units:
                    msg += " Unit id: " + unit_id + ','
                    msg += " Unit name: " + get_unit_name(unit_id) + ','
                raise serializers.ValidationError(msg, code='invalid')
            if len(units) < 1:
                raise serializers.ValidationError("User has no unit", code='invalid')
            elif len(units) == 1:
                unit_id = units[0]
                result["unit_id"] = unit_id

        elif unit_id not in units:
            raise serializers.ValidationError("Bad unit", code='invalid')

        else:
            result["unit_id"] = unit_id
        return result

    def validate(self, attrs):
        """
        Validate the APIKeys and the unit (if the unit is given)
        """
        result = {}

        # Get required parameters
        access_key = attrs.get('access_key')
        secret_key = attrs.get('secret_key')

        # Check API Keys exist and return username
        username = ApiKeyHandler.validate(access=access_key, secret=secret_key)

        # Unit is given ?
        unit_id = None
        if 'unit_id' in attrs:
            unit_id = attrs.get('unit_id')

        # Manage PATCH
        if self.partial:

            if unit_id:
                # check if the unit exists
                if is_unit_exist(unit_id):
                    result["unit_id"] = unit_id
                else:
                    raise serializers.ValidationError("Unit doesn't exist", code='invalid')
            else:
                raise serializers.ValidationError("Unit not found", code='invalid')

            schema_id = self.instance
            sciper = get_sciper(username)

            if Rancher.validate(schema_id, sciper) or is_db_admin(user_id=sciper, unid_id=unit_id):
                return result
            else:
                raise serializers.ValidationError("User is not authorized to acces to this schema", code='invalid')

        # Manage POST
        else:

            if username:
                result["username"] = username

                # If unit is given, check if user belongs to this unit
                # If no unit is given, try to associate schema and unit
                result = SchemaSerializer._manage_units(username, unit_id, result)

            if 'username' not in result or 'unit_id' not in result:
                raise serializers.ValidationError("Invalid APIKeys", code='invalid')

            return result

    def create(self, validated_data):
        """
        Now we have validated data. So we can create schema.
        """

        # Ldap search to find sciper from username
        sciper = get_sciper(validated_data["username"])

        unit_id = None
        if "unit_id" in validated_data:
            unit_id = validated_data['unit_id']

        schema = Rancher.create_mysql_stack(sciper, unit_id)

        return {
            "connection_string": schema["connection_string"],
            "mysql_cmd": schema["mysql_cmd"],
            "unit_id": schema["unit_id"],
            "schema_id": schema["schema_id"]
        }

    def update(self, schema_id, validated_data):
        """
        Now we have validated data. So we can update schema.
        """
        schema = Rancher.get_schema(schema_id)

        if "unit_id" in validated_data:
            unit_id = validated_data['unit_id']
            Rancher.update_schema(schema_id, unit_id)
            schema = Rancher.get_schema(schema_id)

        return schema
