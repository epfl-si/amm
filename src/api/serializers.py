from rest_framework import serializers


class KeySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    public_key = serializers.CharField()
    private_key = serializers.CharField()

    def create(self, validated_data):

        # Ajout de la clé dans redis
        return self.public_key + self.private_key
