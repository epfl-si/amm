"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import auth

from rest_framework import serializers

from .apikeyhandler import ApiKeyHandler
from .rancher import Rancher
from .utils import get_sciper, get_units


class KeySerializer(serializers.Serializer):
    """
    API Key Serializer
    """
    username = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)

    def validate(self, attrs):
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

        key = ApiKeyHandler.generate_keys(validated_data["username"])
        return key


class SchemaSerializer(serializers.Serializer):
    """
    Schema Serializer
    """
    access_key = serializers.CharField(max_length=256)
    secret_key = serializers.CharField(max_length=256)
    unit = serializers.CharField(max_length=256)

    def validate(self, attrs):
        access_key = attrs.get('access_key')
        secret_key = attrs.get('secret_key')

        unit = None
        if 'unit' in attrs:
            unit = attrs.get('unit')

        result = {}
        username = ApiKeyHandler.validate(access=access_key, secret=secret_key)
        if username:
            result["username"] = username

            if not unit:
                units = get_units(username)

                if len(units) > 1:
                    return serializers.ValidationError("User has more one unit", code='authorization')
                if len(units) < 1:
                    return serializers.ValidationError("User has no unit", code='authorization')
                elif len(units) == 1:
                    unit = units[0]
                    result["unit"] = unit

        if not result:
            raise serializers.ValidationError("Invalid APIKeys", code='authorization')

        return result

    def create(self, validated_data):
        # Ldap search to find sciper from username
        sciper = get_sciper(validated_data["username"])

        unit = None
        if "unit" in validated_data:
            unit = validated_data['unit']

        schema = Rancher.create_mysql_stack(sciper, unit)

        return {
            "connection_string": schema["connection_string"],
            "mysql_cmd": schema["mysql_cmd"]
        }
