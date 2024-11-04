from functools import wraps

import django_ratelimit.decorators
from django.conf import settings
from rest_framework.response import Response


def json_response(message=None, data=None, status_code=200):
    return Response({"message": message, "data": data}, status=status_code)


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
