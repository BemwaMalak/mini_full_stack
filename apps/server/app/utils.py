from functools import wraps

import django_ratelimit.decorators
import rest_framework.views
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from authentication.enums import Message


def json_response(message=None, data=None, status_code=200):
    return Response({"message": message, "data": data}, status=status_code)


def exception_handler(exc, context):
    response = rest_framework.views.exception_handler(exc, context)

    if response is not None:
        if response.status_code == HTTP_401_UNAUTHORIZED:
            response.data = {
                "message": Message.UNAUTHORIZED.value,
                "data": None,
                "status_code": HTTP_401_UNAUTHORIZED,
            }
        elif response.status_code == HTTP_403_FORBIDDEN:
            response.data = {
                "message": Message.FORBIDDEN.value,
                "data": None,
                "status_code": HTTP_403_FORBIDDEN,
            }

    return response


def ratelimit(*args, **kwargs):
    """
    A decorator that applies ratelimit only when settings.DEBUG is False.
    """

    def decorator(view_func):
        if settings.RATE_LIMIT_ENABLED:
            # If in development, return the view function unmodified
            @wraps(view_func)
            def _wrapped_view(*args, **kwargs):
                return view_func(*args, **kwargs)

            return _wrapped_view
        else:
            # In production, apply the ratelimit decorator
            return django_ratelimit.decorators.ratelimit(*args, **kwargs)(view_func)

    return decorator
