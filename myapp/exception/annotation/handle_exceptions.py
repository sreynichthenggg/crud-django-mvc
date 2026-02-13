from functools import wraps

from rest_framework.response import Response

from ..exception_advices import ExceptionAdvices


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            response = ExceptionAdvices.handle(exc, context={})
            if response is None:
                raise
            if isinstance(response, Response):
                return response
            return response

    return wrapper
