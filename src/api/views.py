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
from .serializers import KeySerializer, SchemaSerializer, PasswordSerializer
from .utils import get_sciper, get_units, get_username, render_https_url
from .accred import is_db_admin, get_accreditations_units


@api_view()
def api_root(request, format=None):

    return Response({
        'version': render_https_url(reverse('version-detail', request=request, format=format)),
        'apikeys': render_https_url(reverse('apikey-list', request=request, format=format)),
        'schemas': render_https_url(reverse('schema-list', request=request, format=format)),
        'schemas-by-user': render_https_url(reverse(
            'schema-list-by-user',
            args=["133134"],
            request=request,
            format=format)
        ),
        'schemas-by-unit': render_https_url(reverse(
            'schema-list-by-unit',
            args=["13030"],
            request=request,
            format=format)
        ),
    })


class CommonView(APIView):
    def __init__(self):
        self.apikey_handler = ApiKeyHandler()
        self.rancher = Rancher()


class UserList(CommonView):

    def get(self, request):
        """
        Return http response with 404 status
        """
        return Response("Users not found", status=status.HTTP_404_NOT_FOUND)


class UserDetail(CommonView):

    def get(self, request, user_id):
        """
        Return http response with 404 status
        """
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)


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


class SchemaDetailPassword(CommonView):

    def post(self, request, schema_id):

        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():

            data = {
                "schema_id": schema_id
            }
            schema = serializer.save(**data)

            return Response(schema, status=status.HTTP_200_OK)

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
        message: This user isn't allowed to access to the schema
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

                # Get the complete information of schema
                schema = Rancher.get_schema(schema_id)

                # Get the unit of the schema
                unit_id = schema["unit_id"]

                # Check if the schema belongs to the user
                # Or
                # Check if the user is dbadmin of the schema's unit
                if Rancher.validate(schema_id, sciper) or is_db_admin(user_id=sciper, unid_id=unit_id):
                    return Response(schema, status=status.HTTP_200_OK)

                return Response("This user isn't allowed to access to the schema", status=status.HTTP_403_FORBIDDEN)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, schema_id):
        """
        Delete the schema 'schema_id'
        ---
        Response messages:
        - code: 200
        message: OK
        - code: 403
        message: Invalid APIKey
        - code: 403
        message: This user isn't allowed to access to the schema
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

                # Get the complete information of schema
                schema = Rancher.get_schema(schema_id)

                # Get the unit of the schema
                unit_id = schema["unit_id"]

                # Check if the schema belongs to the user
                # Or
                # Check if the user is dbadmin of the schema's unit
                if Rancher.validate(schema_id, sciper) or is_db_admin(user_id=sciper, unid_id=unit_id):

                    Rancher.delete_schema(schema_id)
                    return Response("The schema " + schema_id + " has been deleted", status=status.HTTP_200_OK)

                return Response("This user isn't allowed to access to the schema", status=status.HTTP_403_FORBIDDEN)

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
        if serializer.is_valid(raise_exception=True):
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
                stacks = self.rancher.get_schemas_by_user(sciper)
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


class SchemaListByUser(CommonView):

    def get(self, request, user_id):
        """
        Return the list of schemas by user
        ---
        Response messages:
          - code: 200
            message: OK
          - code: 403
            message: Invalid APIKey
          - code: 403
            message: This user isn't allowed to access to these schemas
          - code 404
            message: Access key or secret key no found
        """
        try:
            username = self.apikey_handler.validate(
                request.query_params['access_key'],
                request.query_params['secret_key']
            )
            if username:

                # if the user is the user in URL parameter
                sciper = get_sciper(username)
                if user_id == sciper:
                    schemas = Rancher.get_schemas_by_user(sciper)
                    return Response(schemas, status=status.HTTP_200_OK)

                else:
                    units = get_accreditations_units(username=get_username(user_id))

                    # if the user is dbadmin
                    if len(units) == 1:

                        unit_id = units[0]

                        if is_db_admin(user_id=sciper, unit_id=unit_id):
                            schemas = Rancher.get_schemas_by_unit_and_user(unit_id=unit_id, user_id=user_id)
                            return Response(schemas, status=status.HTTP_200_OK)

                    elif len(units) > 1:
                        pass

                    else:
                        return Response("This user isn't allowed to access to these schemas",
                                        status=status.HTTP_403_FORBIDDEN)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)


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

                sciper = get_sciper(username)
                user_units = get_units(username)

                # Check if user belongs to unit
                # Or
                # Check if the user is dbadmin of this unit
                if (str(unit_id) not in user_units) and (not is_db_admin(user_id=sciper, unit_id=unit_id)):
                    return Response("User not authorised in this unit", status=status.HTTP_403_FORBIDDEN)

                else:
                    if unit_id in user_units:
                        schemas = Rancher.get_schemas_by_unit_and_user(unit_id, sciper)
                    elif is_db_admin(user_id=sciper, unit_id=unit_id):
                        schemas = Rancher.get_schemas_by_unit(unit_id)

                return Response(schemas, status=status.HTTP_200_OK)

            return Response("Invalid APIKey", status=status.HTTP_403_FORBIDDEN)

        except MultiValueDictKeyError:
            return Response("Access key or secret key no found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, unit_id):
        """
        Create a new schema
        ---
        Response messages:
        - code: 200
          message: OK
        - code: 403
          message: Invalid APIKey
        """

        data = request.data
        data["unit"] = unit_id

        serializer = SchemaSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            schema = serializer.save()
            return Response(schema, status=status.HTTP_200_OK)

        return Response("Invalid APIKeys", status=status.HTTP_403_FORBIDDEN)
