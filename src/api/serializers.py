import coreapi
from rest_framework import serializers


class KeySerializer(serializers.Serializer):

    access_key = serializers.CharField(max_length=256)
    secret_key = serializers.CharField(max_length=256)

    def create(self, validated_data):

        the_key = self.apikey_handler.generate_keys(validated_data['username'])

        return the_key

