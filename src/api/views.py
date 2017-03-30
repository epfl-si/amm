"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from config.settings import base

from .apikeyhandler import ApiKeyHandler
from .filters import APIKeyFilterBackend
from .rancher import Rancher
from .serializers import KeySerializer, SchemaSerializer
from .utils import get_sciper


@api_view()
def api_root(request, format=None):
    return Response({
        'apikeys': reverse('apikeys', request=request, format=format),
        'schemas': reverse('schemas', request=request, format=format),
        'version': reverse('version', request=request, format=format)
    })


class CommonView(APIView):
    def __init__(self):
        self.apikey_handler = ApiKeyHandler()
        self.rancher = Rancher()


class KeysView(CommonView):
    filter_backends = (APIKeyFilterBackend,)

    def get_serializer(self):
        """
        Define the serializer for API Keys view
        Used by swagger documentation
        """
        return KeySerializer()

    def get(self, request):
        """
        Returns the user's API keys
        ---
        Response messages:
          - code: 200
            message: OK
          - code: 403
            message: Invalid APIKey
        """

        # first we check the key
        username = self.apikey_handler.validate(
            request.GET.get('access_key', None),
            request.GET.get('secret_key', None)
        )

        if username:
            keys = self.apikey_handler.get_keys(username)
            return Response(keys, status=status.HTTP_200_OK)

        return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
        Create a new API key
        ---
        Response messages:
        - code: 200
          message: OK
        - code: 401
          message: Authentication failed
        """
        serializer = KeySerializer(data=request.data)

        if serializer.is_valid():
            key = serializer.save()

            return Response(key.get_values(), status=status.HTTP_200_OK)
        else:
            return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)


class SchemasView(CommonView):
    filter_backends = (APIKeyFilterBackend,)

    def get_serializer(self):
        """
        Define the schema serializer
        Used by swagger documentation
        """
        return SchemaSerializer()

    def get(self, request):
        """
        Returns the user's schemas
        ---
        Response messages:
        - code: 200
          message: OK
        - code: 403
          message: Invalid APIKey
        """

        username = self.apikey_handler.validate(
            request.GET.get('access_key', None),
            request.GET.get('secret_key', None)
        )
        if username:
            sciper = get_sciper(username)
            stacks = self.rancher.get_schemas(sciper)
            return Response(stacks, status=status.HTTP_200_OK)

        return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
        Create a new schema
        ---
        Response messages:
        - code: 200
          message: OK
        - code: 403
          message: Invalid APIKey
        """
        serializer = SchemaSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            schema = serializer.save()
            return Response(schema, status=status.HTTP_200_OK)
        else:
            return Response("Invalid APIKeys", status=status.HTTP_403_FORBIDDEN)


class VersionView(APIView):
    def get(self, request):
        """
        Returns the current API version
        ---
        Response messages:
        - code: 200
          message: OK
        """
        return Response(base.VERSION, status=status.HTTP_200_OK)
