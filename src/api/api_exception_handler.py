from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response:

        if 'non_field_errors' in response.data:
            msg = response.data['non_field_errors'][0]
            response.data.pop('non_field_errors')
            response.data = msg

        response.status_code = HTTP_403_FORBIDDEN

    return response
