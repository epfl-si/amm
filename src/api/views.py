"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.utils.datastructures import MultiValueDictKeyError

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
        'apikeys': reverse('apikey-list', request=request, format=format),
        'schemas': reverse('schema-list', request=request, format=format),
        'version': reverse('version-detail', request=request, format=format),
        'schemas-by-unit': reverse('schema-list-by-unit', args=["13030"], request=request, format=format),
    })


class CommonView(APIView):
    def __init__(self):
        self.apikey_handler = ApiKeyHandler()
        self.rancher = Rancher()


class UnitList(CommonView):

    def get(self, request):
        """
        Return http response with 404 status
        """
        return Response("Units not found", status=status.HTTP_404_NOT_FOUND)


class UnitDetail(CommonView):

    def get(self, request, unit_id):
        """
        Return http response with 404 status
        """
        return Response("Unit not found", status=status.HTTP_404_NOT_FOUND)


class SchemaListByUnit(CommonView):

    def get(self, request, unit_id):
        """
        Return the list of schemas by unit
        ---
        Response messages:
          - code: 200
            message: OK
          - code: 403
            message: Invalid APIKey
          - code 404
            message: Access key or secret key no found
        """
        try:
            username = self.apikey_handler.validate(
                request.query_params['access_key'],
                request.query_params['secret_key']
            )
            if username:
                schemas = Rancher.get_schemas_by_unit(unit_id)
                return Response(schemas, status=status.HTTP_200_OK)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)


class APIKeyList(CommonView):

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
          - code: 404
            message: Access key or secret key no found
        """

        try:
            username = self.apikey_handler.validate(
                request.query_params['access_key'],
                request.query_params['secret_key']
            )

            if username:
                keys = self.apikey_handler.get_keys(username)
                return Response(keys, status=status.HTTP_200_OK)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)

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

        return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)


class SchemaDetail(CommonView):

    filter_backends = (APIKeyFilterBackend,)

    def get(self, request, schema_id):
        """
        Return the schema 'schema_id'
        ---
        Response messages:
        - code: 200
        message: OK
        - code: 403
        message: Invalid APIKey
        - code: 403
        message: Schema doesn't belong to this user
        - code: 404
        message: Access key or secret key no found
        """
        try:
            username = self.apikey_handler.validate(
                request.query_params['access_key'],
                request.query_params['secret_key']
            )
            if username:
                sciper = get_sciper(username)

                # Check if the schema belongs to the user
                if Rancher.validate(schema_id, sciper):

                    # Get the complete information of schema
                    schema = Rancher.get_schema(schema_id)
                    return Response(schema, status=status.HTTP_200_OK)

                return Response("Schema doesn't belong to this user", status=status.HTTP_403_FORBIDDEN)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, schema_id):
        """
        Update partially the schema 'schema_id'
        ---
        Response messages:
        - code: 200
        message: OK
        - code: 403
        message: Invalid APIKey
        """
        serializer = SchemaSerializer(instance=schema_id, data=request.data, partial=True)
        if serializer.is_valid():
            # update
            schema = serializer.save()
            return Response(schema, status=status.HTTP_200_OK)

        return Response("Invalid APIKeys", status=status.HTTP_403_FORBIDDEN)


class SchemaList(CommonView):

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
        - code 404
          message: Access key or secret key no found
        """
        try:
            username = self.apikey_handler.validate(
                request.query_params['access_key'],
                request.query_params['secret_key']
            )
            if username:
                sciper = get_sciper(username)
                stacks = self.rancher.get_schemas(sciper)
                return Response(stacks, status=status.HTTP_200_OK)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)

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

        return Response("Invalid APIKeys", status=status.HTTP_403_FORBIDDEN)


class VersionDetail(APIView):

    def get(self, request):
        """
        Returns the current API version
        ---
        Response messages:
        - code: 200
          message: OK
        """
        return Response(base.VERSION, status=status.HTTP_200_OK)
