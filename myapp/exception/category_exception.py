from rest_framework import status


class CategoryException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors=None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors
