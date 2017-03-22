"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import auth

from rest_framework import serializers

from .apikeyhandler import ApiKeyHandler
from .rancher import Rancher
from .utils import get_sciper


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

    def validate(self, attrs):
        access_key = attrs.get('access_key')
        secret_key = attrs.get('secret_key')

        result = {}
        username = ApiKeyHandler.validate(access=access_key, secret=secret_key)
        if username:
            result["username"] = username

        if not result:
            raise serializers.ValidationError("Invalid APIKeys", code='authorization')

        return result

    def create(self, validated_data):
        # Ldap search to find sciper from username
        sciper = get_sciper(validated_data["username"])

        schema = Rancher.create_mysql_stack(sciper)

        return {
            "connection_string": schema["connection_string"],
            "mysql_cmd": schema["mysql_cmd"]
        }
