from django.middleware.csrf import CsrfViewMiddleware
from django.utils.decorators import decorator_from_middleware_with_args


class ExtractCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Get the CSRF token from the cookie named 'csrftoken'
        request.META["HTTP_X_CSRFTOKEN"] = request.COOKIES.get("csrftoken")
        return super().process_view(request, callback, callback_args, callback_kwargs)


csrf_protect = decorator_from_middleware_with_args(ExtractCsrfMiddleware)
