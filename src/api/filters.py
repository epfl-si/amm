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
                location='query',
                required=True,
                type='string'
            ),
            coreapi.Field(
                name='secret_key',
                location='query',
                required=True,
                type='string'
            ),
        ]
