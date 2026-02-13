from rest_framework import status as _status


class HttpStatus:
    OK = _status.HTTP_200_OK
    CREATED = _status.HTTP_201_CREATED
    BAD_REQUEST = _status.HTTP_400_BAD_REQUEST
    NOT_FOUND = _status.HTTP_404_NOT_FOUND
    INTERNAL_SERVER_ERROR = _status.HTTP_500_INTERNAL_SERVER_ERROR
