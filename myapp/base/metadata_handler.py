from dataclasses import dataclass
from functools import wraps

from ..exception import CategoryException


@dataclass(frozen=True)
class Metadata:
    user_id: str | None = None


def _get_user_id(request) -> str | None:
    user_id = (
        request.headers.get("X-User-Id")
        or request.META.get("HTTP_X_USER_ID")
    )
    if user_id is None:
        return None
    if isinstance(user_id, int):
        return str(user_id)
    if isinstance(user_id, str) and user_id.strip():
        return user_id.strip()
    return None


def metadata_handler(required_user_id: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if hasattr(arg, "META"):
                    request = arg
                    break
            if request is None:
                request = kwargs.get("request")
            if request is None:
                raise CategoryException("Request not found", status_code=400)

            user_id = _get_user_id(request)
            if required_user_id and not user_id:
                raise CategoryException("user_id is required", status_code=400)

            kwargs["metadata"] = Metadata(user_id=user_id)
            return func(*args, **kwargs)

        return wrapper

    return decorator
