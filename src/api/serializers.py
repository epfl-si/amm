from rest_framework import serializers

import auth
from api.apikeyhandler import ApiKeyHandler


class KeySerializer(serializers.Serializer):

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

        apikey_handler = ApiKeyHandler()

        key = apikey_handler.generate_keys(validated_data["username"])

        return key


class SchemaSerializer(serializers.Serializer):

    access_key = serializers.CharField(max_length=256)
    secret_key = serializers.CharField(max_length=256)

    def create(self, validated_data):

        the_key = self.apikey_handler.generate_keys(validated_data['username'])

        return the_key

