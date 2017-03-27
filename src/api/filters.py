"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import coreapi
from rest_framework.filters import BaseFilterBackend


class APIKeyFilterBackend(BaseFilterBackend):
    """
    APIKey filter to configure access_key and private_key fiels in swagger documentation
    """

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='access_key',
                required=True,
                location='query',
                schema='schema',
                description='The access key (public part)',
                type='string',
                example='ex',
            ),
            coreapi.Field(
                name='secret_key',
                required=True,
                location='query',
                schema='schema',
                description='The secret key (private part)',
                type='string',
                example='ex',
            ),
        ]
